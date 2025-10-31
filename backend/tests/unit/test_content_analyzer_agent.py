"""
Tests for Content Analyzer Agent.
"""
import pytest
from app.agents.content_analyzer import ContentAnalyzerAgent


class TestContentAnalyzerAgent:
    """Test Content Analyzer Agent."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return ContentAnalyzerAgent()
    
    def test_extract_hashtags(self, analyzer):
        """Test hashtag extraction."""
        text = "This is a #test post with #python and #telegram"
        hashtags = analyzer.extract_hashtags(text)
        
        assert "#test" in hashtags
        assert "#python" in hashtags
        assert "#telegram" in hashtags
        assert len(hashtags) == 3
    
    def test_extract_hashtags_empty(self, analyzer):
        """Test hashtag extraction from empty text."""
        hashtags = analyzer.extract_hashtags("")
        assert hashtags == []
        
        hashtags = analyzer.extract_hashtags(None)
        assert hashtags == []
    
    def test_extract_mentions(self, analyzer):
        """Test mention extraction."""
        text = "Check out @user1 and @user2 for more info"
        mentions = analyzer.extract_mentions(text)
        
        assert "@user1" in mentions
        assert "@user2" in mentions
        assert len(mentions) == 2
    
    def test_extract_links(self, analyzer):
        """Test link extraction."""
        text = "Visit https://example.com and http://test.org for more"
        links = analyzer.extract_links(text)
        
        assert "https://example.com" in links
        assert "http://test.org" in links
    
    def test_extract_links_invalid(self, analyzer):
        """Test that invalid URLs are filtered out."""
        text = "Invalid url: not-a-url and https://valid.com"
        links = analyzer.extract_links(text)
        
        assert "https://valid.com" in links
        assert "not-a-url" not in links
    
    def test_calculate_engagement_rate(self, analyzer):
        """Test engagement rate calculation."""
        rate = analyzer.calculate_engagement_rate(1000, 50)
        assert rate == 0.05
        
        rate = analyzer.calculate_engagement_rate(100, 10)
        assert rate == 0.1
    
    def test_calculate_engagement_rate_zero_views(self, analyzer):
        """Test engagement rate with zero views."""
        rate = analyzer.calculate_engagement_rate(0, 10)
        assert rate is None
    
    def test_estimate_reading_time(self, analyzer):
        """Test reading time estimation."""
        text = " ".join(["word"] * 200)  # 200 words
        time = analyzer.estimate_reading_time(text, words_per_minute=200)
        
        assert time == 60  # 1 minute
    
    def test_classify_content_type(self, analyzer):
        """Test content type classification."""
        # Mixed content
        content_type = analyzer.classify_content_type(
            "photo",
            "Check this out",
            ["https://example.com/image.jpg", "https://example.com/video.mp4"]
        )
        assert content_type == "mixed"
        
        # Link
        content_type = analyzer.classify_content_type(
            "text",
            "Check https://example.com",
            None
        )
        assert content_type == "link"
        
        # Photo gallery
        content_type = analyzer.classify_content_type(
            "photo",
            "Photos",
            ["https://example.com/1.jpg", "https://example.com/2.jpg"]
        )
        assert content_type == "photo_gallery"
    
    def test_categorize_content(self, analyzer):
        """Test content categorization."""
        category = analyzer.categorize_content("Новая новость для вас")
        assert category == "news"
        
        category = analyzer.categorize_content("Реклама нашего продукта")
        assert category == "advertisement"
        
        category = analyzer.categorize_content("Tutorial on how to use it")
        assert category == "educational"
        
        category = analyzer.categorize_content("Funny joke here")
        assert category == "entertainment"
    
    def test_categorize_content_no_match(self, analyzer):
        """Test categorization with no matching keywords."""
        category = analyzer.categorize_content("Random text without keywords")
        assert category is None
    
    def test_analyze_post(self, analyzer):
        """Test complete post analysis."""
        post_data = {
            "post_id": "123",
            "text": "Check out #python #coding at https://example.com. @user1",
            "views": 1000,
            "likes": 50,
            "content_type": "text",
            "media_urls": None
        }
        
        analyzed = analyzer.analyze_post(post_data)
        
        assert "#python" in analyzed["hashtags"]
        assert "#coding" in analyzed["hashtags"]
        assert "@user1" in analyzed["mentions"]
        assert "https://example.com" in analyzed["links"]
        assert analyzed["engagement_rate"] == 0.05
        assert analyzed["reading_time"] > 0
    
    def test_analyze_posts_batch(self, analyzer):
        """Test batch analysis."""
        posts = [
            {
                "post_id": "1",
                "text": "#test",
                "views": 100,
                "likes": 10,
                "content_type": "text",
                "media_urls": None
            },
            {
                "post_id": "2",
                "text": "#python",
                "views": 200,
                "likes": 20,
                "content_type": "text",
                "media_urls": None
            }
        ]
        
        analyzed = analyzer.analyze_posts_batch(posts)
        
        assert len(analyzed) == 2
        assert analyzed[0]["hashtags"] == ["#test"]
        assert analyzed[1]["hashtags"] == ["#python"]

