"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.settings import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Check connection before using
    pool_size=10,        # Number of connections to keep in pool
    max_overflow=20,     # Maximum overflow connections
    echo=settings.DEBUG  # Log SQL queries if debug is on
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize database - create tables.
    Should be called at application startup.
    """
    # Import all models here to ensure they're registered with Base
    from core import models  # noqa
    
    Base.metadata.create_all(bind=engine)
