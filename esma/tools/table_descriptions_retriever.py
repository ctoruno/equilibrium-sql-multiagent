"""
Tool for retrieving table descriptions from markdown files and listing available tables.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from esma.prompts.prompt_loader import PromptLoader
from esma.utils.bigquery_client import BigQueryClient


class TableDescriptionRetrieverInput(BaseModel):
    """Input schema for TableDescriptionRetriever tool."""
    database: Literal["enaho", "geih"] = Field(description="Target database")


class TableDescriptionRetriever(BaseTool):
    """
    Tool for retrieving table descriptions and listing available tables.
    Combines markdown documentation with actual BigQuery table availability.
    """
    
    name: str = "table_description_retriever"
    description: str = """
    Retrieve table information for the specified database.
    Returns:
    - List of available tables in BigQuery
    - Markdown descriptions of tables and their relationships
    - Identification of any discrepancies between documentation and actual tables
    Use this to understand what tables are available and their business context.
    """
    args_schema = TableDescriptionRetrieverInput
    
    
    def _run(self, database: str) -> str:
        """
        Execute table information retrieval.
        
        Returns:
            JSON string with table listings and descriptions
        """
        response = {
            "database": database,
            "available_tables": [],
            "table_descriptions": "",
            "error": None,
            "IMPORTANT_NOTE": ""
        }
        
        try:
            client = BigQueryClient.get_client(database)
            available_tables = client.db.get_usable_table_names()
            response["available_tables"] = sorted(available_tables)
            response["IMPORTANT_NOTE"] = f"Use these table names EXACTLY as listed. DO NOT add '{database}.' prefix in SQL queries."
        except Exception as e:
            response["error"] = f"Failed to retrieve BigQuery tables: {str(e)}"
        
        try:
            prompt_loader = PromptLoader(database)
            table_descriptions = prompt_loader.load_table_descriptions()
            response["table_descriptions"] = table_descriptions
        except FileNotFoundError as e:
            response["error"] = f"Failed to load table descriptions: {str(e)}"
        
        return json.dumps(response, indent=2)