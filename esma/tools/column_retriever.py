"""
Column Retriever Tool using VoyageAI and Pinecone.
"""

import json
from typing import List, Dict, Optional, Literal

import voyageai
from pydantic import BaseModel, Field, PrivateAttr
from langchain.tools import BaseTool
from pinecone import Pinecone

from esma.config.settings import settings

class ColumnRetrieverInput(BaseModel):
    """Input schema for ColumnRetriever tool."""
    query: str = Field(description="Natural language query to search for relevant columns")
    database: Literal["enaho", "geih"] = Field(description="Database name ('enaho' or 'geih')")
    selected_tables: List[str] = Field(description="List of table IDs to filter by")


class ColumnRetriever(BaseTool):
    """
    Tool for retrieving relevant columns from Pinecone vector database using VoyageAI embeddings.
    Handles table filtering and returns structured results with error handling.
    """
    
    name: str = "column_retriever"
    description: str = """
    Retrieve relevant database columns based on a natural language query.
    Use this when you need to find specific columns from selected tables
    to generate SQL queries. Returns column metadata including names,
    descriptions, data types, and valid values.
    """
    args_schema = ColumnRetrieverInput

    _voyage_client: voyageai.Client = PrivateAttr()
    _pinecone_client: Pinecone = PrivateAttr()
    _similarity_threshold: float = PrivateAttr()
    _max_results: int = PrivateAttr()
    _embedding_model: str = PrivateAttr()
    

    def __init__(self):
        """Initialize VoyageAI and Pinecone clients."""
        super().__init__()
        self._voyage_client = voyageai.Client(api_key=settings.voyageai_api_key)
        self._pinecone_client = Pinecone(api_key=settings.pinecone_api_key)
        self._similarity_threshold = settings.similarity_threshold
        self._max_results = settings.max_column_retrieval_results
        self._embedding_model = settings.embedding_model
    

    def _run(self, query: str, database: str, selected_tables: List[str]) -> str:
        """
        Execute the column retrieval tool.
        
        Returns:
            JSON string with retrieval results
        """
        
        database_index = settings.pc_indexes.get(database)
        database_namespaces = f"{database_index}-columns"

        if not query.strip():
            return self._format_response({
                "success": False,
                "columns": [],
                "error": "Query cannot be empty"
            })
        
        if not selected_tables:
            return self._format_response({
                "success": False,
                "columns": [],
                "error": "At least one table must be selected"
            })
        
        try:
            query_embedding = self._generate_embedding(query)
            
            if not query_embedding:
                return self._format_response({
                    "success": False,
                    "columns": [],
                    "error": "Empty query embedding",
                })
                
        except Exception as e:
            return self._format_response({
                "success": False,
                "columns": [],
                "error": f"Embedding generation failed: {str(e)}"
            })
        
        try:
            print(f"Searching Pinecone index '{database_index}' in namespace '{database_namespaces}' for tables {selected_tables}")
            search_results = self._search_pinecone(
                database_index,
                database_namespaces,
                query_embedding,
                selected_tables
            )
            
        except Exception as e:
            return json.dumps(
                {
                    "success": False,
                    "columns": [],
                    "error": f"Pinecone search failed: {str(e)}"
                }, 
                indent=2
            )
        
        filtered_columns = [
            result for result in search_results 
            if result.get('score', 0) >= self._similarity_threshold
        ]
        
        columns = []
        for result in filtered_columns:
            if "metadata" in result:
                column_info = {
                    "table_id": result["metadata"].get("table_id"),
                    "column_name": result["metadata"].get("column_name"),
                    "description": result["metadata"].get("description"),
                    "data_type": result["metadata"].get("data_type"),
                    "business_meaning": result["metadata"].get("business_meaning"),
                    "valid_values": result["metadata"].get("valid_values", {}),
                    "similarity_score": result.get("score")
                }
                columns.append(column_info)
        
        return json.dumps(
            {
                "success": True,
                "columns": columns,
                "error": None
            }, 
            indent=2
        )
    
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using VoyageAI."""
        try:
            response = self._voyage_client.embed(
                texts=[text], 
                model = self._embedding_model
            )
            return response.embeddings[0]
        except Exception:
            return None
    

    def _search_pinecone(
            self,
            database_index: str, 
            database_namespaces: str,
            query_embedding: List[float], 
            selected_tables: List[str]
    ) -> List[Dict]:
        """Search Pinecone for relevant columns."""

        index_name = database_index
        namespace = database_namespaces
        
        index = self._pinecone_client.Index(index_name)        
        table_filter = {
            "table_id": {"$in": selected_tables}
        }
        
        response = index.query(
            vector=query_embedding,
            top_k=self._max_results,
            namespace=namespace,
            filters=table_filter,
            include_metadata=True
        )
        
        return response.get("matches", [])
    
    
    def _format_response(self, response_dict: Dict) -> str:
        """Format response as JSON string for LLM consumption."""
        
        return json.dumps(response_dict, indent=2)