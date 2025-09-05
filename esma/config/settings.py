from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    voyageai_api_key: str
    pinecone_api_key: str
    
    # BigQuery
    gcp_project_id: str
    google_application_credentials: Optional[str] = None
    enaho_dataset: str = "enaho_2024"
    geih_dataset: str = "geih_2024"
    
    # Pinecone
    enaho_index_name: str = "enaho-2024"
    geih_index_name: str = "geih-2024"
    
    # LLM Settings
    default_model: str = "openai:gpt-5"
    max_tokens: int = 10000
    temperature: float = 0.1
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()