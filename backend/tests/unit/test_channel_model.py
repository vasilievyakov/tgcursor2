"""
Tests for Channel model.
"""
import pytest
from sqlalchemy.orm import Session
from app.models.channel import Channel
from datetime import datetime


class TestChannelModel:
    """Test Channel model."""
    
    def test_create_channel(self, db_session: Session):
        """Test creating a channel."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel",
            parse_mode="new_only"
        )
        db_session.add(channel)
        db_session.commit()
        
        assert channel.id is not None
        assert channel.channel_username == "test_channel"
        assert channel.channel_name == "Test Channel"
        assert channel.parse_mode == "new_only"
        assert channel.is_active is True
    
    def test_channel_unique_username(self, db_session: Session):
        """Test that channel username must be unique."""
        channel1 = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel1)
        db_session.commit()
        
        channel2 = Channel(
            channel_username="test_channel",
            channel_name="Another Channel"
        )
        db_session.add(channel2)
        
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_channel_timestamps(self, db_session: Session):
        """Test that timestamps are set correctly."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel)
        db_session.commit()
        
        assert channel.created_at is not None
        assert channel.updated_at is not None
        assert isinstance(channel.created_at, datetime)
        assert isinstance(channel.updated_at, datetime)

