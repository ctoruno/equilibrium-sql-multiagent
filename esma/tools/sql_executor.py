"""
SQL Executor tool for executing validated SQL queries against BigQuery
"""

import json
import logging
from typing import Literal, Dict, Any, Type

from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from esma.utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)


class SQLExecutorInput(BaseModel):
    """Input schema for SQLExecutor tool."""
    sql_query: str = Field(
        description="Validated SQL query to execute against the database"
    )
    database: Literal["enaho", "geih", "ephc", "enemdu"] = Field(
        description="Target database to execute the query against"
    )


class SQLExecutor(BaseTool):
    """
    Tool for executing validated SQL queries against BigQuery databases.
    This tool assumes the query has already been validated by the SchemaValidator.
    Returns query results or error information.
    """
    
    name: str = "sql_executor"
    description: str = """
    Execute a validated SQL query against the specified database.
    Use this after the query has been validated by the schema_validator.
    Returns the query results as structured data or an error message if execution fails.
    """
    args_schema: Type[BaseModel] = SQLExecutorInput
    
    
    def _run(self, sql_query: str, database: str) -> str:
        """
        Execute the SQL query and return results.
        
        Args:
            sql_query: The validated SQL query to execute
            database: The target database ("enaho", "geih", "ephc")
            
        Returns:
            JSON string with execution results or error information
        """
        
        if not sql_query.strip():
            return self._format_response({
                "success": False,
                "error": "SQL query cannot be empty",
                "results": None
            })
        
        try:
            client = BigQueryClient.get_client(database)
            
            logger.info(f"Executing query on {database} database")
            
            results = client.execute_query(sql_query)
            
            return self._format_response({
                "success": True,
                "error": None,
                "results": results,
                "database": database,
                "query_executed": sql_query
            })
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Query execution failed: {error_msg}")
            
            error_type = self._classify_error(error_msg)
            
            return self._format_response({
                "success": False,
                "error": error_msg,
                "error_type": error_type,
                "results": None,
                "database": database,
                "query_attempted": sql_query
            })
    
    
    def _classify_error(self, error_msg: str) -> str:
        """
        Classify the error type for better agent handling.
        
        Args:
            error_msg: The error message string
            
        Returns:
            Error classification
        """
        error_lower = error_msg.lower()
        
        if "timeout" in error_lower:
            return "TIMEOUT"
        elif "permission" in error_lower or "access denied" in error_lower:
            return "PERMISSION_ERROR"
        elif "quota" in error_lower or "rate limit" in error_lower:
            return "QUOTA_EXCEEDED"
        elif "connection" in error_lower or "network" in error_lower:
            return "CONNECTION_ERROR"
        elif "syntax" in error_lower:
            return "SYNTAX_ERROR"
        elif "not found" in error_lower or "does not exist" in error_lower:
            return "RESOURCE_NOT_FOUND" 
        else:
            return "EXECUTION_ERROR"
    
    
    def _format_response(self, response_dict: Dict[str, Any]) -> str:
        """
        Format response as JSON string for LLM consumption.
        
        Args:
            response_dict: Dictionary containing response data
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(response_dict, indent=2)