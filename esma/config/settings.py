import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    """Configuration settings for ESMA SQL Agent"""
    author: str = "Carlos Toruno"

    # API Keys
    # openai_api_key: str
    voyageai_api_key: str
    pinecone_api_key: str

    # BigQuery
    gcp_project_id: str
    google_application_credentials: Optional[str] = None
    dataset_ids: Dict[str, str] = {
        "enaho": "enaho_2024",
        "geih": "geih_2024"
    }

    # SQL Settings
    sql_result_limit: int = 500
    max_retries: int = 3

    # Pinecone & VoyageAI
    similarity_threshold: float = 0.25
    max_column_retrieval_results: int = 7
    max_docs_retrieval_results: int = 25
    pc_indexes: Dict[str, str] = {
        "enaho": "enaho-2024",
        "geih": "geih-2024"
    }
    embedding_model: str = "voyage-3.5"

    # LLM Settings
    # default_model: str = "openai:gpt-5"
    default_model: str = "google_vertexai:gemini-2.5-pro"
    max_tokens: int = 10000
    temperature: float = 0.1

    summarizer_model: str = "google_vertexai:gemini-2.5-flash"
    summarizer_max_tokens: int = 2500
    summarizer_temperature: float = 0.3
    summarizer_token_threshold: int = 500000
    messages_to_keep: int = 3

    # LangSmith
    # langsmith_tracing: bool
    # langsmith_endpoint: str
    # langsmith_project: str
    # langsmith_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
os.environ["GOOGLE_CLOUD_PROJECT"] = settings.gcp_project_id
