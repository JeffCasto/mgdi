import os
from typing import Optional

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Database
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./mgdi.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Model defaults
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    
    # Streaming
    STREAM_CHUNK_SIZE: int = 1024
    STREAM_TIMEOUT: int = 30
    
config = Config()
