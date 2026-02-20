from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGODB_URI: str
    OLLAMA_BASE_URL: Optional[str] = None
    OLLAMA_MODEL: str = "llama3.1"
    LOG_LEVEL: str = "INFO"
    API_KEY: Optional[str] = None
    SEED_TOKEN: str
    MODEL_VERSION: str = "rb-v1"
    POLICY_VERSION: str = "policy-v1"
    
    # Feature flags
    ENABLE_HF_EMBEDDINGS: bool = False
    HF_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
