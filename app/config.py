"""Configurações da aplicação"""
from pydantic_settings import BaseSettings
from typing import List
import os
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb+srv://projeto5mlet:projetofiap@apiembrapa.wcmp3fv.mongodb.net/?retryWrites=true&w=majority&appName=apiEmbrapa")
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # API Settings
    API_ENV: str = os.getenv("API_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS - permite todas as origens em produção para facilitar testes
    CORS_ORIGINS: List[str] = ["*"] if os.getenv("API_ENV") == "production" else ["http://localhost:3000"]
    
    # Configurações específicas do Render
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 