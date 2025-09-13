"""
Tool for retrieving table descriptions from markdown files.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from esma.prompts.prompt_loader import PromptLoader


class TableDescriptionRetrieverInput(BaseModel):
    """Input schema for TableDescriptionRetriever tool."""
    user_query: str = Field(description="Natural language user query")
    database: Literal["enaho", "geih"] = Field(description="Target database")


class TableDescriptionRetriever(BaseTool):
    """
    Tool for retrieving table descriptions from markdown files.
    """
    
    name: str = "table_description_retriever"
    description: str = """
    Retrieve table descriptions for the specified database.
    Use this to understand the schema and relationships between tables.
    Returns the content of the markdown file as a string.
    """
    args_schema = TableDescriptionRetrieverInput
    
    
    def _run(self, user_query: str, database: str) -> str:
        """
        Execute the schema validation.
        
        Returns:
            JSON string with validation results
        """
        try:
            prompt_loader = PromptLoader(database)
            table_descriptions = prompt_loader.load_table_descriptions()
            return table_descriptions
        
        except FileNotFoundError as e:
            return json.dumps({
                "error": f"Failed to load table descriptions: {e}"
            })