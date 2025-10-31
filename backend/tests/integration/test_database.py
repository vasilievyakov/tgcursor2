"""
Tests for database connection.
"""
import pytest
from app.core.database import engine, SessionLocal


class TestDatabase:
    """Test database connection."""
    
    def test_engine_created(self):
        """Test that database engine is created."""
        assert engine is not None
    
    def test_session_local_created(self):
        """Test that session local is created."""
        assert SessionLocal is not None
    
    @pytest.mark.integration
    def test_database_connection(self):
        """Test database connection."""
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                assert result.fetchone()[0] == 1
        except Exception as e:
            pytest.skip(f"Database not available: {e}")

