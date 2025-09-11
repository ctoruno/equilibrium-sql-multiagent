from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
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
    max_docs_retrieval_results: int = 50
    pc_indexes: Dict[str, str] = {
        "enaho": "enaho-2024",
        "geih": "geih-2024"
    }
    embedding_model: str = "voyage-3.5"
    
    # LLM Settings
    default_model: str = "openai:gpt-5"
    max_tokens: int = 10000
    temperature: float = 0.1

    # LangSmith
    langsmith_tracing: bool
    langsmith_endpoint: str 
    langsmith_project: str
    langsmith_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()