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
    OPENAI_API_KEY: Optional[str] = None
    ANALYSIS_MODEL: str = "gpt-4o-mini"  # Small, fast model for analysis
    GENERATION_MODEL: str = "gpt-4o"     # Large, reasoning model for generation
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
