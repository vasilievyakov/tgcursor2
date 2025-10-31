"""
Integration tests for Content Analyzer Agent.
"""
import pytest
from app.agents.content_analyzer import ContentAnalyzerAgent
from app.models.post import Post
from app.core.database import SessionLocal
from datetime import datetime


@pytest.mark.integration
class TestContentAnalyzerIntegration:
    """Integration tests for Content Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return ContentAnalyzerAgent()
    
    def test_analyze_post_from_database(self, analyzer, db_session):
        """Test analyzing post stored in database."""
        from app.models.channel import Channel
        
        # Create channel
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel)
        db_session.commit()
        
        # Create post
        post = Post(
            post_id="12345",
            channel_id=channel.id,
            text="Check out #python #coding at https://example.com. @user1",
            date=datetime.utcnow(),
            content_type="text",
            views=1000,
            likes=50
        )
        db_session.add(post)
        db_session.commit()
        
        # Analyze post
        post_data = {
            "post_id": post.post_id,
            "text": post.text,
            "views": post.views,
            "likes": post.likes,
            "content_type": post.content_type,
            "media_urls": post.media_urls
        }
        
        analyzed = analyzer.analyze_post(post_data)
        
        # Update post with analyzed data
        post.hashtags = analyzed["hashtags"]
        post.mentions = analyzed["mentions"]
        post.links = analyzed["links"]
        post.engagement_rate = analyzed["engagement_rate"]
        db_session.commit()
        
        # Verify
        updated_post = db_session.query(Post).filter_by(id=post.id).first()
        assert updated_post.hashtags == ["#python", "#coding"]
        assert updated_post.engagement_rate == 0.05
    
    def test_performance_batch_analysis(self, analyzer):
        """Test performance of batch analysis."""
        import time
        
        posts = [
            {
                "post_id": str(i),
                "text": f"Test post #{i} with #hashtag",
                "views": 100 * i,
                "likes": 10 * i,
                "content_type": "text",
                "media_urls": None
            }
            for i in range(100)
        ]
        
        start_time = time.time()
        analyzed = analyzer.analyze_posts_batch(posts)
        end_time = time.time()
        
        assert len(analyzed) == 100
        assert (end_time - start_time) < 10  # Should complete in less than 10 seconds

