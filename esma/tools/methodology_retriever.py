"""
Methodology Retriever Tool using VoyageAI and Pinecone for documentation search.
"""

import json
from typing import List, Dict, Optional, Literal

import voyageai
from pydantic import BaseModel, Field, PrivateAttr
from langchain.tools import BaseTool
from pinecone import Pinecone

from esma.config.settings import settings


class MethodologyRetrieverInput(BaseModel):
    """Input schema for MethodologyRetriever tool."""
    query: str = Field(
        description="Natural language query about methodology, data collection, sampling, or survey design"
    )
    database: Literal["enaho", "geih"] = Field(
        description="Database name ('enaho' or 'geih')"
    )


class MethodologyRetriever(BaseTool):
    """
    Tool for retrieving relevant methodology documentation from Pinecone vector database.
    Searches chunked PDF documentation for information about data collection, sampling,
    survey design, and other methodological aspects.
    """
    
    name: str = "methodology_retriever"
    description: str = """
    Retrieve relevant methodology documentation based on a natural language query.
    Use this when users ask about:
    - Data collection methods
    - Sampling procedures
    - Survey design and structure
    - Variable definitions and coding
    - Statistical methodology
    - Data quality and limitations
    Returns relevant documentation chunks to answer methodological questions.
    """
    args_schema = MethodologyRetrieverInput

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
        self._max_results = settings.max_docs_retrieval_results
        self._embedding_model = settings.embedding_model


    def _run(self, query: str, database: str) -> str:
        """
        Execute the methodology documentation retrieval.
        
        Returns:
            JSON string with retrieval results
        """
        
        database_index = settings.pc_indexes.get(database)
        documentation_namespace = f"{database_index}-documentation"
        
        if not query.strip():
            return self._format_response({
                "success": False,
                "chunks": [],
                "error": "Query cannot be empty"
            })

        max_chunks = self._max_results

        try:
            query_embedding = self._generate_embedding(query)
            
            if not query_embedding:
                return self._format_response({
                    "success": False,
                    "chunks": [],
                    "error": "Failed to generate embedding for query",
                })
                
        except Exception as e:
            return self._format_response({
                "success": False,
                "chunks": [],
                "error": f"Embedding generation failed: {str(e)}"
            })
        
        try:
            print(f"Searching Pinecone index '{database_index}' in namespace '{documentation_namespace}' for methodology")
            search_results = self._search_documentation(
                database_index,
                documentation_namespace,
                query_embedding,
                max_chunks
            )
            
        except Exception as e:
            return self._format_response({
                "success": False,
                "chunks": [],
                "error": f"Documentation search failed: {str(e)}"
            })
        
        filtered_chunks = [
            result for result in search_results 
            if result.get("score", 0) >= self._similarity_threshold
        ]
        
        documentation_chunks = []
        for result in filtered_chunks:
            chunk_info = {
                "chunk_id": result.get("id"),
                "content": result.get("metadata", {}).get("text", ""),
                "source": result.get("metadata", {}).get("source", ""),
                "page_number": result.get("metadata", {}).get("page", None),
                "section": result.get("metadata", {}).get("section", None),
                "similarity_score": result.get("score")
            }
            documentation_chunks.append(chunk_info)
        
        # Add summary information
        response_data = {
            "success": True,
            "database": database,
            "query": query,
            "chunks_retrieved": len(documentation_chunks),
            "chunks": documentation_chunks,
            "error": None
        }
        
        if not documentation_chunks:
            response_data["warning"] = (
                f"No documentation chunks found with similarity >= {self._similarity_threshold}. "
                "Consider rephrasing the query or checking if this topic is covered in the documentation."
            )
        
        return self._format_response(response_data)
    
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using VoyageAI."""
        try:
            response = self._voyage_client.embed(
                texts=[text], 
                model=self._embedding_model
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Embedding generation error: {e}")
            return None
    

    def _search_documentation(
            self,
            database_index: str, 
            documentation_namespace: str,
            query_embedding: List[float],
            max_chunks: int
    ) -> List[Dict]:
        """Search Pinecone for relevant documentation chunks."""
        
        index = self._pinecone_client.Index(database_index)
        
        # No filter needed - we want all documentation chunks
        response = index.query(
            vector=query_embedding,
            top_k=max_chunks,
            namespace=documentation_namespace,
            include_metadata=True
        )
        
        return response.get("matches", [])
    
    
    def _format_response(self, response_dict: Dict) -> str:
        """Format response as JSON string for LLM consumption."""
        return json.dumps(response_dict, indent=2)