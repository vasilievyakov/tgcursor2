"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tgcursor2"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Telegram API
    TELEGRAM_API_ID: str = ""
    TELEGRAM_API_HASH: str = ""
    
    # Application
    SECRET_KEY: str = "change-me-in-production"
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Export limits
    MAX_EXPORT_ROWS: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

