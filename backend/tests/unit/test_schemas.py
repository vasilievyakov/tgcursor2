"""
Tests for Pydantic schemas.
"""
import pytest
from datetime import datetime
from app.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate
from app.schemas.post import PostCreate, PostResponse


class TestChannelSchemas:
    """Test Channel schemas."""
    
    def test_channel_create_schema(self):
        """Test ChannelCreate schema."""
        channel_data = {
            "channel_username": "test_channel",
            "channel_name": "Test Channel",
            "parse_mode": "new_only"
        }
        channel = ChannelCreate(**channel_data)
        assert channel.channel_username == "test_channel"
        assert channel.channel_name == "Test Channel"
        assert channel.parse_mode == "new_only"
    
    def test_channel_create_invalid_parse_mode(self):
        """Test that invalid parse_mode is rejected."""
        channel_data = {
            "channel_username": "test_channel",
            "channel_name": "Test Channel",
            "parse_mode": "invalid_mode"
        }
        with pytest.raises(Exception):
            ChannelCreate(**channel_data)
    
    def test_channel_response_schema(self):
        """Test ChannelResponse schema."""
        channel_data = {
            "id": 1,
            "channel_username": "test_channel",
            "channel_name": "Test Channel",
            "parse_mode": "new_only",
            "channel_avatar_url": None,
            "subscribers_count": 0,
            "description": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True,
            "last_parsed_at": None
        }
        channel = ChannelResponse(**channel_data)
        assert channel.id == 1
        assert channel.channel_username == "test_channel"


class TestPostSchemas:
    """Test Post schemas."""
    
    def test_post_create_schema(self):
        """Test PostCreate schema."""
        post_data = {
            "post_id": "12345",
            "channel_id": 1,
            "text": "Test post",
            "date": datetime.utcnow(),
            "content_type": "text",
            "views": 100,
            "likes": 10
        }
        post = PostCreate(**post_data)
        assert post.post_id == "12345"
        assert post.channel_id == 1
        assert post.content_type == "text"
    
    def test_post_create_invalid_content_type(self):
        """Test that invalid content_type is rejected."""
        post_data = {
            "post_id": "12345",
            "channel_id": 1,
            "text": "Test post",
            "date": datetime.utcnow(),
            "content_type": "invalid_type"
        }
        with pytest.raises(Exception):
            PostCreate(**post_data)

