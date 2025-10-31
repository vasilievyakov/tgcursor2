"""
Conftest for pytest fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.core.config import settings


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    engine = create_engine(
        settings.DATABASE_URL.replace("tgcursor2", "tgcursor2_test"),
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

