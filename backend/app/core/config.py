"""
Configuration settings for IdentiFace Studio
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "IdentiFace Studio"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Forensic Face Sketch Construction and Recognition"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000"
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://identiface:password@localhost/identiface_db"
    
    # Redis (Optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS: bool = False
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    
    # Face Recognition Settings
    FACE_RECOGNITION_TOLERANCE: float = 0.6
    FACE_DETECTION_MODEL: str = "hog"  # 'hog' or 'cnn'
    NUM_JITTERS: int = 1
    FACE_ENCODING_MODEL: str = "large"  # 'small' or 'large'
    
    # Matching Settings
    MIN_SIMILARITY_SCORE: float = 0.4
    MAX_RESULTS: int = 50
    
    # Sketch Settings
    DEFAULT_CANVAS_WIDTH: int = 800
    DEFAULT_CANVAS_HEIGHT: int = 1000
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    
    # Storage
    STORAGE_TYPE: str = "local"  # 'local' or 's3'
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = ""
    AWS_REGION: str = "us-east-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/sketches", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/suspects", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/temp", exist_ok=True)
