"""Application configuration settings"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Carely AI - Healthcare Assistant"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = Field(default=False)
    
    # Security
    SECRET_KEY: str = Field(
        default="CHANGE-THIS-IN-PRODUCTION",
        description="Secret key for JWT tokens - MUST be set in .env for production"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./carely.db",
        description="Database connection URL"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    
    # AI/ML Models
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    
    # Healthcare specific
    MAX_APPOINTMENT_DAYS_AHEAD: int = 90
    SUPPORT_EMAIL: str = "support@carely-ai.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars from parent directories


settings = Settings()


