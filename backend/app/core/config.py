from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Driven Threat Detection System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "development_password"
    POSTGRES_DB: str = "threat_detection"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///dev.db"
    
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/threat_detection"
    
    # Security
    SECRET_KEY: str = "development_secret_key_please_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ML Model Settings
    MODEL_THRESHOLD: float = 0.8
    ANOMALY_DETECTION_INTERVAL: int = 300
    
    # SIEM Integration
    WAZUH_CONFIG: Dict[str, Any] = {
        "host": "localhost",
        "port": 55000,
        "user": "wazuh",
        "password": None
    }
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
