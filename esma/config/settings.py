import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    """Configuration settings for ESMA SQL Agent"""
    author: str = "Carlos Toruno"

    # API Keys
    voyageai_api_key: str
    pinecone_api_key: str

    # BigQuery
    gcp_project_id: str
    gcp_region: str = "us-east1"
    google_application_credentials: Optional[str] = None
    dataset_ids: Dict[str, str] = {
        "enaho": "enaho_2024",
        "geih": "geih_2024"
    }

    # SQL
    sql_result_limit: int = 500
    max_retries: int = 3

    # Pinecone & VoyageAI
    similarity_threshold: float = 0.25
    max_docs_retrieval_results: int = 25
    pc_indexes: Dict[str, str] = {
        "enaho": "enaho-2024",
        "geih": "geih-2024"
    }
    embedding_model: str = "voyage-3.5"

    # VertexAI
    max_column_retrieval_results: int = 15
    vertex_location: str = "us-east1"
    vertex_api_endpoint: Dict[str, str] = {
        "enaho": "1799297254.us-east1-514700908055.vdb.vertexai.goog",
        "geih": "2141955479.us-east1-514700908055.vdb.vertexai.goog"
    }
    vertex_index_endpoints: Dict[str, str] = {
        "enaho": "projects/514700908055/locations/us-east1/indexEndpoints/3366058091412979712",
        "geih": "projects/514700908055/locations/us-east1/indexEndpoints/5723692496341434368"
    }
    vertex_deployed_indexes: Dict[str, str] = {
        "enaho": "enaho_2024_columns_dp",
        "geih": "geih_2024_columns_dp"
    }
    vertex_embedding_model: str = "gemini-embedding-001"
    vertex_embedding_dimension: int = 3072

    # LLM Settings
    default_model: str = "google_vertexai:gemini-2.5-pro"
    max_tokens: int = 10000
    temperature: float = 0.1

    summarizer_model: str = "google_vertexai:gemini-2.5-flash"
    summarizer_max_tokens: int = 2500
    summarizer_temperature: float = 0.3
    summarizer_token_threshold: int = 500000
    messages_to_keep: int = 3

    # Local LangGraph Platform Development
    langsmith_tracing: bool
    langsmith_endpoint: str
    langsmith_project: str
    langsmith_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
if settings.google_application_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
os.environ["GOOGLE_CLOUD_PROJECT"] = settings.gcp_project_id
