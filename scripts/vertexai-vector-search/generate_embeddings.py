"""
Generate embeddings for a database data dictionary using VertexAI
"""

import os
import json
import logging
import argparse
from dataclasses import dataclass
from typing import Dict, List, Any
from dotenv import load_dotenv

from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud import storage
from google.cloud import aiplatform
import vertexai

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


AVAILABLE_DATABASES = ["enaho-2024", "geih-2024", "ephc-2024", "enemdu-2024"]


@dataclass
class DatabaseDetails:
    """Store infrastructure details"""
    name: str
    source_bucket: str


class ColumnIndexPopulator:
    """Populates column schema data into VertexAI Vector Search indexes"""

    DATABASES = {
        "enaho-2024": DatabaseDetails(
            name="enaho-2024",
            source_bucket="sql-multiagent-enaho-2024"
        ),
        "geih-2024": DatabaseDetails(
            name="geih-2024",
            source_bucket="sql-multiagent-geih-2024"
        ),
        "ephc-2024": DatabaseDetails(
            name="ephc-2024",
            source_bucket="sql-multiagent-ephc-2024"
        ),
        "enemdu-2024": DatabaseDetails(
            name="enemdu-2024",
            source_bucket="sql-multiagent-enemdu-2024"
        )
    }

    def __init__(self, database: str):
        """
        Initialize the populator for a specific database
        
        Args:
            database: Database name (enaho-2024, geih-2024, ephc-2024)
        """
        self.database = database
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.region = os.getenv("GCP_REGION", "us-east1")
        self.source_bucket = self.DATABASES[database].source_bucket
        self.target_bucket = "sql-multiagent-column-vectors"
        
        aiplatform.init(project=self.project_id, location=self.region)
        vertexai.init(project=self.project_id, location=self.region)
        self.storage_client = storage.Client()
        self.vertex_client = genai.Client(
            vertexai=True, 
            project=self.project_id, 
            location=self.region
        )
        
        self.embedding_model = "gemini-embedding-001"
        
        logger.info(f"Initialized ColumnIndexPopulator for {database}")
    
    
    def load_schema_from_gcs(self, file_path: str) -> Dict[str, Any]:
        """Load JSON schema file from GCS"""
        try:
            bucket = self.storage_client.bucket(self.source_bucket)
            blob = bucket.blob(file_path)
            content = blob.download_as_text()
            schema_data = json.loads(content)
            logger.info(f"Loaded schema from {file_path}")
            return schema_data
        
        except Exception as e:
            logger.error(f"Failed to load schema from {file_path}: {e}")
            return None
    
    
    def prepare_column_text(self, column_info: Dict[str, Any]) -> str:
        """Create text for embedding from column information"""

        parts = []
        
        if desc := column_info.get("description", "").strip():
            parts.append(desc)
        
        if meaning := column_info.get("business_meaning", "").strip():
            parts.append(meaning)
        
        if valid_values := column_info.get("valid_values", {}):
            if isinstance(valid_values, dict):
                categories = [f"{k}={v}" for k, v in valid_values.items()]
                if categories:
                    parts.append(f"Values: {', '.join(categories)}")
        
        return " | ".join(filter(None, parts))
    
    
    def process_table_columns(self, schema_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process all columns from a schema file"""
        
        processed_columns = []
        
        for table_name, table_info in schema_data.get("tables", {}).items():
            columns = table_info.get("columns", {})
            
            for column_name, column_info in columns.items():
                column_name_clean = column_name.replace("Ñ", "N").replace("$", "_")
                embedding_text = self.prepare_column_text(column_info)
                
                if not embedding_text:
                    logger.warning(f"Skipping column {column_name_clean} in {table_name} due to lack of description")
                    continue
                
                record = {
                    "id": f"{table_name}_{column_name_clean}",
                    "text": embedding_text,
                    "metadata": {
                        "table_id": table_name,
                        "column_name": column_name_clean,
                        "data_type": column_info.get("data_type", ""),
                        "description": column_info.get("description", "")
                    }
                }
                
                processed_columns.append(record)
        
        return processed_columns
    
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings using VertexAI text embedding model"""
        
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            try:
                response = self.vertex_client.models.embed_content(
                    model=self.embedding_model,
                    contents=batch_texts,
                    config=EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT",
                        output_dimensionality=3072
                    )
                )
                
                for embedding in response.embeddings:
                    all_embeddings.append(embedding.values)
                
                logger.info(f"Generated embeddings for batch {i//batch_size + 1}")
                
            except Exception as e:
                logger.error(f"Failed to generate embeddings: {e}")
                raise
        
        return all_embeddings
    

    def upload_to_gcs(self, records: List[Dict[str, Any]]) -> None:
        """
        Upload records to GCS as a JSONL file.
        """
        try:
            jsonl_lines = []
            for record in records:
                datapoint = {
                    "id": record["id"],
                    "embedding": record["embedding"],
                    "restricts": [
                        {"namespace": "database", "allow": [self.database]},
                        {"namespace": "table_id", "allow": [record["metadata"]["table_id"]]}
                    ],
                    "embedding_metadata": {
                        "column_name": record["metadata"]["column_name"],
                        "text": record["text"],
                        "table_id": record["metadata"]["table_id"],
                        "data_type": record["metadata"]["data_type"]
                    }
                }
                jsonl_lines.append(json.dumps(datapoint))
            
            jsonl_content = "\n".join(jsonl_lines)
            
            file_name = f"{self.database}-vectors.json"
            bucket = self.storage_client.bucket(self.target_bucket)
            blob = bucket.blob(file_name)
            blob.upload_from_string(jsonl_content, content_type="application/jsonl")

            gcs_uri = f"gs://{self.target_bucket}/{file_name}"
            logger.info(f"Uploaded JSONL to {gcs_uri}")
            
        except Exception as e:
            logger.error(f"Failed to upload to GCS: {e}")
            raise
    
    
    def run_pipeline(self) -> None:
        """
        Run the full pipeline to generate and upload column embeddings
        """
        
        logger.info(f"Starting column population for {self.database}")
        
        bucket = self.storage_client.bucket(self.source_bucket)
        blobs = bucket.list_blobs(prefix="dictionaries/")
        json_files = [blob.name for blob in blobs if blob.name.endswith(".json")]
        
        if not json_files:
            logger.warning(f"No schema files found for {self.database}")
            return
        
        all_columns = []
        for file_path in json_files:
            schema_data = self.load_schema_from_gcs(file_path)
            if schema_data:
                columns = self.process_table_columns(schema_data)
                all_columns.extend(columns)
                logger.info(f"Processed {len(columns)} columns from {file_path}")
        
        if not all_columns:
            logger.warning("No columns found to process")
            return
        
        logger.info(f"Total columns to process: {len(all_columns)}")
        
        texts = [col["text"] for col in all_columns]
        embeddings = self.generate_embeddings(texts)
        
        for i, col in enumerate(all_columns):
            col["embedding"] = embeddings[i]
        
        self.upload_to_gcs(all_columns)
        
        logger.info(f"✅ Successfully generated column embeddings for {self.database} with {len(all_columns)} records")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Populate column index for a database")
    parser.add_argument("--database", required=True, help="Database name (enaho-2024, geih-2024)")
    
    args = parser.parse_args()
    
    if args.database not in AVAILABLE_DATABASES:
        logger.error("Database must be an available option")
        return
    
    try:
        populator = ColumnIndexPopulator(args.database)
        populator.run_pipeline()
        
    except Exception as e:
        logger.error(f"Failed to populate columns: {e}")
        raise


if __name__ == "__main__":
    main()