"""
Tests for Post model.
"""
import pytest
from sqlalchemy.orm import Session
from app.models.channel import Channel
from app.models.post import Post
from datetime import datetime


class TestPostModel:
    """Test Post model."""
    
    @pytest.fixture
    def channel(self, db_session: Session):
        """Create a test channel."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel)
        db_session.commit()
        return channel
    
    def test_create_post(self, db_session: Session, channel: Channel):
        """Test creating a post."""
        post = Post(
            post_id="12345",
            channel_id=channel.id,
            text="Test post",
            date=datetime.utcnow(),
            content_type="text"
        )
        db_session.add(post)
        db_session.commit()
        
        assert post.id is not None
        assert post.post_id == "12345"
        assert post.channel_id == channel.id
        assert post.text == "Test post"
        assert post.content_type == "text"
    
    def test_post_relationship_with_channel(self, db_session: Session, channel: Channel):
        """Test post relationship with channel."""
        post = Post(
            post_id="12345",
            channel_id=channel.id,
            text="Test post",
            date=datetime.utcnow(),
            content_type="text"
        )
        db_session.add(post)
        db_session.commit()
        
        assert post.channel.id == channel.id
        assert post.channel.channel_username == "test_channel"
        assert len(channel.posts) == 1
    
    def test_post_json_fields(self, db_session: Session, channel: Channel):
        """Test JSON fields in post."""
        post = Post(
            post_id="12345",
            channel_id=channel.id,
            text="Test post",
            date=datetime.utcnow(),
            content_type="photo",
            media_urls=["https://example.com/image.jpg"],
            hashtags=["#test", "#python"],
            mentions=["@user1"],
            links=["https://example.com"]
        )
        db_session.add(post)
        db_session.commit()
        
        assert post.media_urls == ["https://example.com/image.jpg"]
        assert post.hashtags == ["#test", "#python"]
        assert post.mentions == ["@user1"]
        assert post.links == ["https://example.com"]

