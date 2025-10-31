"""
Tests for User model.
"""
import pytest
from sqlalchemy.orm import Session
from app.models.user import User


class TestUserModel:
    """Test User model."""
    
    def test_create_user(self, db_session: Session):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            username="testuser"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.is_admin is False
    
    def test_user_unique_email(self, db_session: Session):
        """Test that user email must be unique."""
        user1 = User(
            email="test@example.com",
            username="user1"
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(
            email="test@example.com",
            username="user2"
        )
        db_session.add(user2)
        
        with pytest.raises(Exception):
            db_session.commit()

