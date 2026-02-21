"""
Configuration settings for VulnGuardian.
Loads from environment variables or .env file.
"""
import os
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "VulnGuardian"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(False, env="DEBUG")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    
    # Server
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    
    # Database
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field("vulnguardian", env="DB_NAME")
    DB_USER: str = Field("vulnguardian", env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    
    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    
    @property
    def REDIS_URL(self) -> str:
        """Get Redis URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Modules
    ENABLED_MODULES: List[str] = Field(
        ["scanner", "network_map"],
        env="ENABLED_MODULES"
    )
    
    @validator("ENABLED_MODULES", pre=True)
    def parse_enabled_modules(cls, v):
        """Parse comma-separated string to list."""
        if isinstance(v, str):
            return [m.strip() for m in v.split(",")]
        return v
    
    # Scanner settings
    OPENVAS_URL: Optional[str] = Field(None, env="OPENVAS_URL")
    OPENVAS_USER: Optional[str] = Field(None, env="OPENVAS_USER")
    OPENVAS_PASSWORD: Optional[str] = Field(None, env="OPENVAS_PASSWORD")
    
    TRIVY_ENABLED: bool = Field(True, env="TRIVY_ENABLED")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FILE: str = str(BASE_DIR / "logs" / "app.log")
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = "HS256"
    
    # 2FA
    TWO_FACTOR_ENABLED: bool = Field(False, env="TWO_FACTOR_ENABLED")
    
    # Backup
    BACKUP_ENABLED: bool = Field(True, env="BACKUP_ENABLED")
    BACKUP_DIR: str = str(BASE_DIR / "data" / "backups")
    BACKUP_RETENTION_DAYS: int = Field(30, env="BACKUP_RETENTION_DAYS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings()
