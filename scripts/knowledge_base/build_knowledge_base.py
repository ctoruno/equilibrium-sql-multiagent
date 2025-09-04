import os
import json
import logging
from io import BytesIO
from typing import Dict, List, Optional, Any

import tiktoken
import PyPDF2
import argparse
from google.cloud import storage
from pinecone import Pinecone, ServerlessSpec
import voyageai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KnowledgeBaseBuilder:
    """Builds the vector knowledge base for SQL agent schema information."""
    
    def __init__(
        self,
        database_name: str,
        gcs_bucket: str,
        doc_type: str,
        pinecone_api_key: Optional[str] = None,
        voyage_api_key: Optional[str] = None,
        embedding_model: str = "voyage-3.5",
        embedding_dimension: int = 1024
    ):
        """
        Initialize the knowledge base builder.
        
        Args:
            database_name: Either 'enaho-2024' or 'geih-2024'
            gcs_bucket: GCS bucket name containing schema files
            doc_type: Document type to process, either "schema" or "documentation"
            pinecone_api_key: Pinecone API key (defaults to env var)
            voyage_api_key: Voyage AI API key (defaults to env var)
            embedding_model: Voyage model to use for embeddings
            embedding_dimension: Dimension of embeddings (voyage-3.5 = 1024)
        """
        
        self.database_name = database_name
        self.gcs_bucket = gcs_bucket
        self.gcs_client = storage.Client()
        self.bucket = self.gcs_client.bucket(gcs_bucket)

        if doc_type not in ["schema", "documentation"]:
            raise ValueError("doc_type must be either 'schema' or 'documentation'")
        else:
            self.doc_type = doc_type
            if self.doc_type == "schema":
                self.prefix = "dictionaries/"
            if self.doc_type == "documentation":
                self.prefix = "metadata/"   
        
        pinecone_key = pinecone_api_key or os.getenv("PINECONE_API_KEY")
        if not pinecone_key:
            raise ValueError("Pinecone API key not found in environment or parameters ❌")
        self.pinecone_client = Pinecone(api_key=pinecone_key)

        voyage_key = voyage_api_key or os.getenv("VOYAGEAI_API_KEY")
        if not voyage_key:
            raise ValueError("Voyage AI API key not found in environment or parameters ❌")
        self.voyage_client = voyageai.Client(api_key=voyage_key)

        self.embedding_model = embedding_model
        self.embedding_dimension = embedding_dimension

        logger.info("KnowledgeBaseBuilder initialized successfully ✅")

    
    def list_target_files(self, file_format: str) -> List[str]:
        """List all files in GCS with given prefix."""
        blobs = self.bucket.list_blobs(prefix=self.prefix)
        target_files = [
            blob.name 
            for blob in blobs 
            if blob.name.endswith(file_format)
        ]
        logger.info(f"Found {len(target_files)} files with prefix '{self.prefix}'")
        return target_files
    

    def load_files_from_gcs(self, file_path: str) -> Dict[str, Any]:
        """
        Load a file from GCS.
        Args:
            file_path: Path to the file in GCS
        """
        
        if self.doc_type == "schema":
            try:
                blob = self.bucket.blob(file_path)
                content = blob.download_as_text()
                schema_data = json.loads(content)
                logger.info(f"Loaded schema from {file_path} ✅")
                return schema_data
            
            except Exception as e:
                logger.error(f"Failed to load schema from {file_path}: {e} ❌")
                raise
        
        if self.doc_type == "documentation":
            try:
                blob = self.bucket.blob(file_path)
                pdf_content = blob.download_as_bytes()
                pdf_stream = BytesIO(pdf_content)            
                pdf_reader = PyPDF2.PdfReader(pdf_stream)
                extracted_text = ""

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    extracted_text += page.extract_text() + "\n"
                logger.info(f"Loaded PDF documentation from {file_path} - {len(pdf_reader.pages)} pages ✅")
                return {
                    "file_path": file_path, 
                    "text": extracted_text.strip(), 
                    "pages": len(pdf_reader.pages)
                }
            
            except Exception as e:
                logger.error(f"Failed to load PDF documentation from {file_path}: {e} ❌")
                raise

    
    def prepare_schema_for_embedding(self, column_info: Dict[str, Any]) -> str:
        """
        Create concatenated text for embedding from column information.
        
        Combines: column_name, description, business_meaning, and valid_values (if available)
        """
        
        parts = []
        
        description = column_info.get("description", "").strip()
        parts.append(description)
        
        business_meaning = column_info.get("business_meaning", "").strip()
        parts.append(business_meaning)
        
        valid_values = column_info.get("valid_values", {})
        if valid_values and isinstance(valid_values, dict):
            categories = []
            for key, value in valid_values.items():
                categories.append(f"{key}={value}")
            if categories:
                parts.append(f"Categories: {', '.join(categories)}")
        
        embedding_text = " | ".join(filter(None, parts))
        return embedding_text
    

    def process_table_columns(self, table_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process all columns from a table and prepare them for embedding.
        
        Args:
            table_data: Single table data from JSON schema
            
        Returns:
            List of processed column records ready for embedding
        """
        
        processed_columns = []
        
        for table_name, table_info in table_data.get("tables", {}).items():
            columns = table_info.get("columns", {})
            
            for column_name, column_info in columns.items():
                
                column_name_clean = (       # ENAHO uses special characters as column headers
                    column_name
                    .replace("Ñ", "N")
                    .replace("$", "_")
                )

                embedding_text = self.prepare_schema_for_embedding(column_info)
                
                metadata = {
                    "table_id": table_name,
                    "column_name": column_name_clean,
                    "description": column_info.get("description", "").strip(),
                    "data_type": column_info.get("data_type", ""),
                    "business_meaning": column_info.get("business_meaning", "")
                }
                
                valid_values = column_info.get("valid_values")
                if valid_values and isinstance(valid_values, dict):
                    metadata["valid_values"] = [f"{k}:{v}" for k, v in valid_values.items()]
                
                record = {
                    "id": f"{table_name}_{column_name_clean}",
                    "embedding_text": embedding_text,
                    "metadata": metadata,
                    "database": self.database_name
                }
                
                processed_columns.append(record)
        
        return processed_columns
    

    def process_pdf_for_embedding(self, pdf_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Preprocess PDF text into chunks for embedding.
        
        Args:
            pdf_data: Dictionary with 'file_path', 'text', and 'pages' keys from load_files_from_gcs
            
        Returns:
            List of chunk records ready for embedding
        """
        
        try:
            text = pdf_data["text"]
            file_name = pdf_data["file_path"].split("/")[-1]
            
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
            
            chunk_size = 650
            overlap = 75
            step_size = chunk_size - (2 * overlap)
            
            chunks = []
            chunk_number = 0
            
            for i in range(0, len(tokens), step_size):
                
                start_idx = max(0, i - overlap)
                end_idx = min(len(tokens), i + chunk_size - overlap)
                
                chunk_tokens = tokens[start_idx:end_idx]                
                chunk_text = encoding.decode(chunk_tokens)
                
                if len(chunk_tokens) < 50:     # Skip very small chunks
                    continue
                    
                record = {
                    "id": f"{self.database_name}_{chunk_number}",
                    "embedding_text": chunk_text.strip(),
                    "metadata": {"source": file_name},
                    "database": self.database_name
                }
                
                chunks.append(record)
                chunk_number += 1
                
                if end_idx >= len(tokens):
                    break
            
            logger.info(f"Created {len(chunks)} chunks from {file_name} ✅")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to preprocess documentation: {e} ❌")
            raise


    def generate_embeddings(self, texts: List[str], batch_size: int = 128) -> List[List[float]]:
        """Generate embeddings for a list of texts using Voyage AI."""
        
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            try:
                response = self.voyage_client.embed(
                    texts=batch_texts,
                    model=self.embedding_model
                )
                
                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)
                
                logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} ✅")
                
            except Exception as e:
                logger.error(f"Failed to generate embeddings for batch starting at {i}: {e} ❌")
                raise
        
        return all_embeddings
    

    def create_pinecone_index(self, index_name: str) -> None:
        """Create Pinecone index if it doesn't exist."""

        if not self.pinecone_client.has_index(index_name):
            self.pinecone_client.create_index(
                index_name,
                dimension = self.embedding_dimension,
                spec = ServerlessSpec(
                    cloud = "aws",
                    region = "us-east-1"
                ),
                metric = "cosine"
            )
            logger.info(f"Index {index_name} created successfully ✅")
        else:
            logger.info(f"Index {index_name} already exists ✅")
        
    
    def upload_to_pinecone(
        self, 
        index_name: str, 
        namespace: str, 
        records: List[Dict[str, Any]], 
        batch_size: int = 100
    ) -> None:
        """Upload embedded records to Pinecone."""
        
        index = self.pinecone_client.Index(index_name, pool_threads=30)
        
        vectors = []
        for record in records:
            vector = {
                "id": record["id"],
                "values": record["embedding"],
                "metadata": record["metadata"]
            }
            vectors.append(vector)
        
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]

            try:
                async_result = index.upsert(vectors=batch, namespace=namespace, async_req=True)
                logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1} to {namespace} ✅")
                print(async_result.get())

            except Exception as e:
                logger.error(f"Failed to upload batch to Pinecone: {e} ❌")
                raise
    

    def build_database_knowledge_base(self) -> None:
        """Build knowledge base for a specific database (ENAHO or GEIH)."""
        
        logger.info(f"Building knowledge base for {self.database_name.upper()}")
        
        chunks = []

        if self.doc_type == "schema":
            target_files = self.list_target_files(file_format = ".json")
            if not target_files:
                logger.warning(f"No files found for {self.database_name}")
                return
                
            for file_path in target_files:
                try:
                    schema_data = self.load_files_from_gcs(file_path)
                    columns = self.process_table_columns(schema_data)
                    chunks.extend(columns)
                    logger.info(f"Processed {len(columns)} columns from {file_path} ✅")
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {e} ❌")
                    continue
            
            if not chunks:
                logger.warning(f"No columns found for {self.database_name}")
                return
            
            logger.info(f"Total columns to process for {self.database_name}: {len(chunks)}")
        
        if self.doc_type == "documentation":
            target_files = self.list_target_files(file_format = ".pdf")
            if not target_files:
                logger.warning(f"No files found for {self.database_name}")
                return
            
            for file_path in target_files:
                try:
                    pdf_data = self.load_files_from_gcs(file_path)
                    chunked_doc = self.process_pdf_for_embedding(pdf_data)
                    chunks.extend(chunked_doc)
                    logger.info(f"Processed {len(chunked_doc)} chunks from {file_path} ✅")
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {e} ❌")
                    continue

        embedding_texts = [chunk["embedding_text"] for chunk in chunks]
        embeddings = self.generate_embeddings(embedding_texts)
        
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i]
        
        self.create_pinecone_index(self.database_name)
        
        if self.doc_type == "schema":
            namespace = f"{self.database_name}-columns"
        if self.doc_type == "documentation":
            namespace = f"{self.database_name}-documentation"

        try:
            self.upload_to_pinecone(self.database_name, namespace, chunks)
            logger.info(f"Successfully built knowledge base for {self.database_name.upper()}: {self.doc_type} ✅ ✅ ✅")
        except Exception as e:
            logger.error(f"Knowledge base build failed: {e} ❌")
            raise


def main():
    """Main function to run the knowledge base builder."""

    parser = argparse.ArgumentParser(description="Build knowledge database for a specific survey.")
    parser.add_argument("--survey", help="Survey name to work with (e.g., 'enaho-2024', 'geih-2024')")
    parser.add_argument("--type", help="Build knowledge database for 'schema' or 'documentation'")
    
    args = parser.parse_args()

    if args.survey not in ["enaho-2024", "geih-2024"]:
        logger.error("Error: Survey must be either 'enaho-2024' or 'geih-2024' ❌")
        return
    if args.type not in ["schema", "documentation"]:
        logger.error("Error: Type must be either 'schema' or 'documentation' ❌")
        return
    
    SURVEY_NAME=args.survey
    TYPE=args.type
    
    if args.survey in ["enaho-2024"]:
        GCS_BUCKET = "sql-multiagent-enaho-2024"
        
    if args.survey in ["geih-2024"]:
        GCS_BUCKET = "sql-multiagent-geih-2024"
    
    builder = KnowledgeBaseBuilder(
        database_name=SURVEY_NAME,
        gcs_bucket=GCS_BUCKET,
        doc_type=TYPE
    )

    try:
        builder.build_database_knowledge_base()
        logger.info("Complete knowledge base build finished successfully ✅ ✅ ✅")
        
    except Exception as e:
        logger.error(f"Knowledge base build failed: {e} ❌")
        raise


if __name__ == "__main__":
    main()