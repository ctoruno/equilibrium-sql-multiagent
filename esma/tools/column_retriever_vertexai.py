"""
Column Retriever Tool using VertexAI Embeddings and Vector Search.
"""

import json
from typing import List, Dict, Optional, Literal

from google import genai
from google.cloud import aiplatform_v1
from google.genai.types import EmbedContentConfig
from pydantic import BaseModel, Field, PrivateAttr
from langchain.tools import BaseTool

from esma.config.settings import settings


class ColumnRetrieverInput(BaseModel):
    """Input schema for ColumnRetriever tool."""
    query: str = Field(description="Natural language query to search for relevant columns")
    database: Literal["enaho", "geih"] = Field(description="Database name ('enaho' or 'geih')")
    selected_tables: List[str] = Field(description="List of table IDs to filter by")


class ColumnRetriever(BaseTool):
    """
    Tool for retrieving relevant columns from VertexAI Vector Search using Gemini embeddings.
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

    _vertex_client: genai.Client = PrivateAttr()
    _vector_search_client: aiplatform_v1.MatchServiceClient = PrivateAttr()
    _max_results: int = PrivateAttr()
    

    def __init__(self):
        """Initialize VertexAI clients."""
        super().__init__()
        
        self._vertex_client = genai.Client(
            vertexai=True,
            project=settings.gcp_project_id,
            location=settings.vertex_location
        )
        self._max_results = settings.max_column_retrieval_results
    

    def _run(self, query: str, database: str, selected_tables: List[str]) -> str:
        """
        Execute the column retrieval tool.
        
        Returns:
            JSON string with retrieval results
        """

        api_endpoint = settings.vertex_api_endpoint.get(database)
        index_endpoint = settings.vertex_index_endpoints.get(database)
        deployed_index_id = settings.vertex_deployed_indexes.get(database)
        
        if not all([api_endpoint, index_endpoint, deployed_index_id]):
            return self._format_response({
                "success": False,
                "columns": [],
                "error": f"Index configuration not found for database: {database}"
            })
        
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
                    "error": "Failed to generate embedding"
                })
                
        except Exception as e:
            return self._format_response({
                "success": False,
                "columns": [],
                "error": f"Embedding generation failed: {str(e)}"
            })
        
        try:
            vector_search_client = aiplatform_v1.MatchServiceClient(
                client_options={"api_endpoint": api_endpoint}
            )
            
            print(f"Searching VertexAI index for database '{database}' with tables {selected_tables}")
            search_results = self._search_vertex_index(
                vector_search_client,
                index_endpoint,
                deployed_index_id,
                query_embedding,
                selected_tables
            )
            
        except Exception as e:
            return self._format_response({
                "success": False,
                "columns": [],
                "error": f"Vector search failed: {str(e)}"
            })
        
        columns = []
        for result in search_results:
            metadata = result.datapoint.embedding_metadata
            column_info = {
                "table_id": metadata.get("table_id"),
                "column_name": metadata.get("column_name"),
                "description": metadata.get("text"),
                "data_type": metadata.get("data_type")
            }
            columns.append(column_info)
                
        return self._format_response({
            "success": True,
            "columns": columns,
            "error": None
        })
    
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using VertexAI Gemini."""
        try:
            response = self._vertex_client.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
                config=EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY", # See: https://ai.google.dev/gemini-api/docs/embeddings?hl=es-419#supported-task-types
                    output_dimensionality=settings.vertex_embedding_dimension
                )
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    

    def _search_vertex_index(
            self,
            vector_search_client: aiplatform_v1.MatchServiceClient,
            index_endpoint: str,
            deployed_index_id: str,
            query_embedding: List[float],
            selected_tables: List[str]
    ) -> List:
        """Search VertexAI Vector Search index."""
        
        restricts = [
            aiplatform_v1.IndexDatapoint.Restriction(
                namespace="table_id",
                allow_list=selected_tables
            )
        ]
        
        datapoint = aiplatform_v1.IndexDatapoint(
            feature_vector=query_embedding,
            restricts=restricts
        )
        
        query = aiplatform_v1.FindNeighborsRequest.Query(
            datapoint=datapoint,
            neighbor_count=self._max_results
        )
        
        request = aiplatform_v1.FindNeighborsRequest(
            index_endpoint=index_endpoint,
            deployed_index_id=deployed_index_id,
            queries=[query],
            return_full_datapoint=True
        )
        
        response = vector_search_client.find_neighbors(request)
        
        if response.nearest_neighbors:
            return response.nearest_neighbors[0].neighbors
        return []
    
    
    def _format_response(self, response_dict: Dict) -> str:
        """Format response as JSON string for LLM consumption."""
        return json.dumps(response_dict, indent=2)