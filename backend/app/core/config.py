import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "BlindSpot AI"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Database
    DATABASE_URL: str = "sqlite:///./blindspot.db"
    
    # Security
    JWT_SECRET: str = "dev_secret_key_jwt_blindspot_2026_super_secure"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AI Engine
    AI_API_KEY: str = ""
    AI_MODEL: str = "llama-3.3-70b-versatile"
    AI_PROVIDER: str = "groq"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
