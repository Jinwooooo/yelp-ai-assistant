from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Yelp AI Assistant"
    DEBUG: bool = True
    
    # Infrastructure
    CASSANDRA_CONTACT_POINTS: str = "localhost"
    CASSANDRA_KEYSPACE: str = "yelp_assistant"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # AI Models
    GEMINI_API_KEY: Optional[str] = None
    ANALYSIS_MODEL: str = "gemini-1.5-flash"  # Small, fast model for analysis
    GENERATION_MODEL: str = "gemini-1.5-pro"  # High-reasoning model for generation
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
