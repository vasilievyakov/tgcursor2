"""
Tests for Filter & Search Agent.
"""
import pytest
from datetime import datetime, timedelta
from app.agents.filter_search import FilterSearchAgent
from app.models.channel import Channel
from app.models.post import Post


class TestFilterSearchAgent:
    """Test Filter & Search Agent."""
    
    @pytest.fixture
    def agent(self, db_session):
        """Create agent instance."""
        return FilterSearchAgent(db_session)
    
    @pytest.fixture
    def test_channel(self, db_session):
        """Create test channel."""
        channel = Channel(
            channel_username="test_channel",
            channel_name="Test Channel"
        )
        db_session.add(channel)
        db_session.commit()
        return channel
    
    @pytest.fixture
    def test_posts(self, db_session, test_channel):
        """Create test posts."""
        posts = []
        base_date = datetime.utcnow()
        
        for i in range(10):
            post = Post(
                post_id=f"post_{i}",
                channel_id=test_channel.id,
                text=f"Test post {i} with #hashtag{i}",
                date=base_date - timedelta(days=i),
                content_type="text" if i % 2 == 0 else "photo",
                views=100 * i,
                likes=10 * i,
                hashtags=[f"#hashtag{i}"]
            )
            db_session.add(post)
            posts.append(post)
        
        db_session.commit()
        return posts
    
    def test_filter_by_date_range(self, agent, test_posts):
        """Test filtering by date range."""
        date_from = datetime.utcnow() - timedelta(days=5)
        date_to = datetime.utcnow()
        
        filters = {
            "date_from": date_from,
            "date_to": date_to
        }
        
        query = agent.db.query(Post)
        filtered_query = agent.filter_posts(query, filters)
        results = filtered_query.all()
        
        assert len(results) <= 6  # Posts from last 5 days
        
        for post in results:
            assert post.date >= date_from
            assert post.date <= date_to
    
    def test_get_filtered_posts_with_pagination(self, agent, test_posts):
        """Test getting filtered posts with pagination."""
        filters = {
            "content_types": ["text"]
        }
        
        result = agent.get_filtered_posts(
            filters=filters,
            page=1,
            page_size=5
        )
        
        assert "posts" in result
        assert "total" in result
        assert "page" in result
        assert "page_size" in result
        assert "total_pages" in result
        
        assert len(result["posts"]) <= 5
        assert result["page"] == 1
        assert result["page_size"] == 5
