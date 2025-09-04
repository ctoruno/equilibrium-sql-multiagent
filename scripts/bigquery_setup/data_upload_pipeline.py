import os
import sys
import tempfile
import logging
from typing import List, Dict

import argparse
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BigQueryCSVUploader:
    def __init__(self, project_id: str, survey: str):
        """
        Initialize the uploader with project and bucket information.
        
        Args:
            project_id: Google Cloud Project ID
            source_bucket: Survey to process
        """

        if survey not in ["enaho-2024", "geih-2024"]:
            logger.error("Error: Survey must be either 'enaho-2024' or 'geih-2024' ❌")
            return
        else:
            self.survey = survey
        
        if self.survey in ["enaho-2024"]:
            self.dataset = "enaho_2024"
            self.bucket_name = "sql-multiagent-enaho-2024"
            self.data_encoding = "latin1"
            self.delimiter = ","

        if self.survey in ["geih-2024"]:
            self.dataset = "geih_2024"
            self.bucket_name = "sql-multiagent-geih-2024"
            self.data_encoding = "utf-8"
            self.delimiter = ";"

        self.project_id = project_id
        self.storage_client = storage.Client(project=project_id)
        self.bigquery_client = bigquery.Client(project=project_id)

        
    def sanitize_column_name(self, column_name: str) -> str:
        sanitized = column_name.replace('Ñ', 'N').replace('$', '_')
        return sanitized
    
    
    def get_csv_files_from_bucket(self, prefix: str) -> List[str]:
        """
        List all CSV files in the bucket.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            List of CSV file names
        """

        bucket = self.storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        
        csv_files = []
        for blob in blobs:
            if blob.name.lower().endswith('.csv'):
                csv_files.append(blob.name)
                
        logger.info(f"Found {len(csv_files)} CSV files in bucket {self.bucket_name}")
        return csv_files
    
    
    def download_and_sanitize_csv(self, csv_file_path: str) -> pd.DataFrame:
        """
        Download CSV from Cloud Storage and sanitize column names.
        
        Args:
            csv_file_path: Path to CSV file in bucket
            
        Returns:
            DataFrame with sanitized column names
        """

        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(csv_file_path)
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp_file:
            blob.download_to_filename(tmp_file.name)
            
            df = pd.read_csv(
                tmp_file.name, 
                encoding=self.data_encoding,
                delimiter=self.delimiter
            )
            
            original_columns = df.columns.tolist()
            sanitized_columns = [self.sanitize_column_name(col) for col in original_columns]
            
            changes = [
                (orig, san) for orig, san in zip(original_columns, sanitized_columns) 
                if orig != san
            ]
            # if changes:
            #     logger.info(f"Column name changes for {csv_file_path}:")
            #     for orig, san in changes:
            #         logger.info(f"  '{orig}' -> '{san}'")
            
            df.columns = sanitized_columns
            
            os.unlink(tmp_file.name)
            
            return df
        
    
    def upload_to_bigquery(self, df: pd.DataFrame, dataset_name: str, table_name: str, 
                          csv_file_path: str) -> bool:
        """
        Upload DataFrame to BigQuery with auto-schema detection.
        
        Args:
            df: DataFrame to upload
            dataset_name: BigQuery dataset name
            table_name: BigQuery table name
            csv_file_path: Original CSV file path (for logging)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            dataset_ref = self.bigquery_client.dataset(dataset_name)
            table_ref = dataset_ref.table(table_name)
            
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                skip_leading_rows=0
            )
            
            job = self.bigquery_client.load_table_from_dataframe(
                df, 
                table_ref, 
                job_config=job_config
            )
            
            job.result()
            
            table = self.bigquery_client.get_table(table_ref)
            logger.info(f"✅ Successfully uploaded {csv_file_path}")
            logger.info(f"   Dataset: {dataset_name}")
            logger.info(f"   Table: {table_name}")
            logger.info(f"   Rows: {table.num_rows:,}")
            logger.info(f"   Columns: {len(table.schema)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to upload {csv_file_path}: {str(e)}")
            return False
    

    def process_all_csvs(self, file_prefix: str = '') -> Dict[str, bool]:
        """
        Process all CSV files in the bucket.
        
        Args:
            file_prefix: Optional prefix to filter files
            
        Returns:
            Dictionary mapping file paths to success/failure status
        """

        csv_files = self.get_csv_files_from_bucket(file_prefix)
        results = {}
        
        total_files = len(csv_files)
        logger.info(f"Starting upload of {total_files} CSV files to BigQuery...")
        
        for i, csv_file_path in enumerate(csv_files, 1):
            logger.info(f"\n[{i}/{total_files}] Processing: {csv_file_path}")
            
            try:
                df = self.download_and_sanitize_csv(csv_file_path)
                logger.info(f"--- Loaded DataFrame: {len(df):,} rows × {len(df.columns)} columns")
                
                file_name = os.path.basename(csv_file_path).replace('.csv', '')
                table_name = file_name.replace('-', '_').replace(' ', '_')
                
                success = self.upload_to_bigquery(df, self.dataset, table_name, csv_file_path)
                results[csv_file_path] = success
                
            except Exception as e:
                logger.error(f"❌ Error processing {csv_file_path}: {str(e)}")
                results[csv_file_path] = False
        
        successful = sum(1 for success in results.values() if success)
        failed = total_files - successful
        
        logger.info(f"\n{'='*60}")
        logger.info("UPLOAD SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total files processed: {total_files}")
        logger.info(f"Successful uploads: {successful}")
        logger.info(f"Failed uploads: {failed}")
        
        if failed > 0:
            logger.info("\nFailed files:")
            for file_path, success in results.items():
                if not success:
                    logger.info(f"  - {file_path}")
        
        return results


def main():
    """
    Main execution function.
    Configure your project settings here.
    """

    parser = argparse.ArgumentParser(description="Build knowledge database for a specific survey.")
    parser.add_argument("--survey", help="Survey name to work with (e.g., 'enaho-2024', 'geih-2024')")
    
    args = parser.parse_args()

    if args.survey not in ["enaho-2024", "geih-2024"]:
        logger.error("Error: Survey must be either 'enaho-2024' or 'geih-2024' ❌")
        return
    
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        logger.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        sys.exit(1)
    
    PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    SURVEY = args.survey
    
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        logger.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        return
    
    uploader = BigQueryCSVUploader(PROJECT_ID, SURVEY)
    results = uploader.process_all_csvs(file_prefix="data/")
    
    failed_count = sum(1 for success in results.values() if not success)
    if failed_count > 0:
        logger.error(f"Upload completed with {failed_count} failures")
        exit(1)
    else:
        logger.info("All uploads completed successfully! 🎉")
        exit(0)


if __name__ == "__main__":
    main()