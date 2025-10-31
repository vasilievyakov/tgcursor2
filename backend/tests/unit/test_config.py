"""
Tests for configuration and basic setup.
"""
import pytest
from app.core.config import settings


class TestConfiguration:
    """Test application configuration."""
    
    def test_settings_loaded(self):
        """Test that settings are loaded."""
        assert settings is not None
    
    def test_database_url_set(self):
        """Test that database URL is set."""
        assert settings.DATABASE_URL is not None
        assert "postgresql" in settings.DATABASE_URL
    
    def test_redis_url_set(self):
        """Test that Redis URL is set."""
        assert settings.REDIS_URL is not None
        assert "redis" in settings.REDIS_URL
    
    def test_allowed_origins_set(self):
        """Test that CORS origins are set."""
        assert len(settings.ALLOWED_ORIGINS) > 0

