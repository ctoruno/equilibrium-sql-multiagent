"""
Schema Gatherer tool for retrieving table schemas and sample data from BigQuery
"""

import json
from typing import Literal, Dict, Any, List

from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from esma.utils.bigquery_client import BigQueryClient
from esma.config.settings import settings


class SchemaGathererInput(BaseModel):
    """Input schema for SchemaGatherer tool."""
    tables: str = Field(
        description="Comma-separated list of table names to get schema for (e.g., 'table1, table2, table3')"
    )
    database: Literal["enaho", "geih", "ephc", "enemdu"] = Field(
        description="Target database"
    )


class SchemaGatherer(BaseTool):
    """
    Tool for gathering detailed schema information and sample data from BigQuery tables.
    Provides column details, data types, and example rows for specified tables.
    """
    
    name: str = "schema_gatherer"
    description: str = """
    Gather detailed schema information and sample data for specific tables. Use the table_description_retriever 
    tool first to see available tables and their descriptions.
    Use this when you need to understand:
    - Column names and data types for specific tables
    - See example data to understand value formats
    - Verify table structure before writing SQL
    Input: comma-separated table names and database
    Returns: schema details and sample rows for each table
    """
    args_schema = SchemaGathererInput
    
    
    def _run(self, tables: str, database: str) -> str:
        """
        Execute schema and sample data gathering.
        
        Returns:
            JSON string with schema information and sample data
        """
        table_list = [t.strip() for t in tables.split(",") if t.strip()]
        
        if not table_list:
            return json.dumps({
                "success": False,
                "error": "No valid table names provided",
                "tables_info": {}
            }, indent=2)
                
        client = BigQueryClient.get_client(database)
        tables_info = {}
        errors = []
        
        for table_name in table_list:
            table_data = {
                "exists": False,
                "schema": "",
                "sample_data": None,
                "row_count": None,
                "error": None
            }
            
            try:
                schema_info = client.get_table_info(table_names=[table_name])
                if schema_info:
                    table_data["exists"] = True
                    table_data["schema"] = schema_info
                    
                    sample_query = f"SELECT * FROM {table_name} LIMIT 5"
                    try:
                        sample_result = client.execute_query(sample_query)
                        table_data["sample_data"] = sample_result
                    except Exception as e:
                        table_data["error"] = f"Could not retrieve sample data: {str(e)}"
                    
                else:
                    table_data["error"] = f"Table '{table_name}' not found in database"
                    errors.append(f"Table '{table_name}' not found")
                    
            except Exception as e:
                table_data["error"] = f"Failed to get table info: {str(e)}"
                errors.append(f"Error with table '{table_name}': {str(e)}")
            
            tables_info[table_name] = table_data
        
        response = {
            "success": len(errors) == 0,
            "database": database,
            "tables_requested": table_list,
            "tables_found": [t for t, info in tables_info.items() if info["exists"]],
            "tables_not_found": [t for t, info in tables_info.items() if not info["exists"]],
            "tables_info": tables_info
        }
        
        if errors:
            response["errors"] = errors
        
        return json.dumps(response, indent=2)