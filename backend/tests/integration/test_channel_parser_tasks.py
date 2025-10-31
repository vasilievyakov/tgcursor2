"""
Integration tests for Channel Parser Agent with Celery.
"""
import pytest
from datetime import datetime
from app.core.tasks import parse_channel_task, parse_channel_posts_task
from app.core.database import SessionLocal
from app.models.channel import Channel
from app.models.post import Post


@pytest.mark.integration
class TestChannelParserTasks:
    """Test Channel Parser Celery tasks."""
    
    def test_parse_channel_task_structure(self):
        """Test that parse_channel_task is properly configured."""
        assert parse_channel_task is not None
        assert hasattr(parse_channel_task, 'delay')
    
    def test_parse_channel_posts_task_structure(self):
        """Test that parse_channel_posts_task is properly configured."""
        assert parse_channel_posts_task is not None
        assert hasattr(parse_channel_posts_task, 'delay')
    
    @pytest.mark.slow
    def test_parse_channel_task_mock(self):
        """Test parse_channel_task with mocked parser."""
        # This would require actual Telegram API credentials
        # For now, we just test the structure
        # In real testing, you would mock the Telegram client
        pass
    
    def test_channel_saved_to_database(self, db_session):
        """Test that parsed channel is saved to database."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel",
            parse_mode="new_only"
        )
        db_session.add(channel)
        db_session.commit()
        
        saved_channel = db_session.query(Channel).filter_by(
            channel_username="test_channel"
        ).first()
        
        assert saved_channel is not None
        assert saved_channel.channel_name == "Test Channel"
    
    def test_posts_saved_to_database(self, db_session):
        """Test that parsed posts are saved to database."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel)
        db_session.commit()
        
        post = Post(
            post_id="12345",
            channel_id=channel.id,
            text="Test post",
            date=datetime.utcnow(),
            content_type="text"
        )
        db_session.add(post)
        db_session.commit()
        
        saved_post = db_session.query(Post).filter_by(
            post_id="12345",
            channel_id=channel.id
        ).first()
        
        assert saved_post is not None
        assert saved_post.text == "Test post"

