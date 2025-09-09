"""
BigQuery client wrapper using SQLAlchemy and LangChain
"""

from typing import Optional, Dict, Any, List
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from langchain_community.utilities import SQLDatabase

from esma.config.settings import settings

logger = logging.getLogger(__name__)

class BigQueryClient:
    """Manages BigQuery connections via SQLAlchemy"""
    
    _instances: Dict[str, 'BigQueryClient'] = {}
    
    def __init__(self, database_name: str):
        """
        Initialize BigQuery client for a specific database
        
        Args:
            database_name: Name of the database (enaho or geih)
        """
        self.database_name = database_name
        self.dataset_id = self._get_dataset_id(database_name)
        self._engine: Optional[Engine] = None
        self._db: Optional[SQLDatabase] = None
        self.sql_result_limit = settings.sql_result_limit

        logger.info(f"BigQueryClient initialized for {self.database_name} ({self.dataset_id})")


    def _get_dataset_id(self, database_name: str) -> str:
        """Get the BigQuery dataset ID for a database"""
        dataset_map = settings.dataset_ids
        return dataset_map.get(database_name, database_name)
    

    @classmethod
    def get_client(cls, database_name: str) -> 'BigQueryClient':
        """
        Get or create a client for a specific database
        
        Args:
            database_name: Name of the database (enaho or geih)
            
        Returns:
            BigQueryClient instance for the database
        """
        if database_name not in cls._instances:
            cls._instances[database_name] = cls(database_name)
        return cls._instances[database_name]
    

    @property
    def engine(self) -> Engine:
        """Get SQLAlchemy engine (lazy initialization)"""

        if self._engine is None:
            connection_string = f"bigquery://{settings.gcp_project_id}/{self.dataset_id}"
            self._engine = create_engine(
                connection_string,
                credentials_path=settings.google_application_credentials
            )
            logger.info(f"SQLAlchemy engine created for {self.database_name} ({self.dataset_id})")
        
        return self._engine
    

    @property
    def db(self) -> SQLDatabase:
        """Get LangChain SQLDatabase wrapper (lazy initialization)"""
        if self._db is None:
            self._db = SQLDatabase(self.engine)
            logger.info(f"LangChain SQLDatabase initialized for {self.database_name}")
        return self._db

    
    def execute_query(self, sql: str) -> str:
        """
        Execute a query using LangChain and return results as string
        
        Args:
            sql: SQL query to execute
        
        Returns:
            String representation of query results
        """
        if self.sql_result_limit and "LIMIT" not in sql.upper():
            sql = f"{sql.rstrip(';')} LIMIT {self.sql_result_limit};"
        
        return self.db.run(sql)
    

    def get_table_info(self, table_names: Optional[List[str]] = None) -> str:
        """
        Get table schema information using LangChain's table_info
        
        Args:
            table_names: Optional list of specific tables to get info for
            
        Returns:
            String with table schema information
        """
        try:
            return self.db.get_table_info(table_names=table_names)
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return ""
    
    
    def validate_tables_exist(self, table_names: List[str]) -> Dict[str, bool]:
        """
        Check if tables exist in the dataset
        
        Args:
            table_names: List of table names to check
        
        Returns:
            Dictionary mapping table names to existence status
        """
        try:
            existing_tables = self.db.get_usable_table_names()
            return {
                table: table in existing_tables 
                for table in table_names
            }
        except Exception as e:
            logger.error(f"Failed to validate tables: {e}")
            return {table: False for table in table_names}