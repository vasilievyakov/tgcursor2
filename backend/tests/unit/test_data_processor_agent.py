"""
Tests for Data Processor Agent.
"""
import pytest
from datetime import datetime
from app.agents.data_processor import DataProcessorAgent
import pytz


class TestDataProcessorAgent:
    """Test Data Processor Agent."""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return DataProcessorAgent()
    
    def test_normalize_date_from_datetime(self, processor):
        """Test date normalization from datetime."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        normalized = processor.normalize_date(dt)
        
        assert normalized.tzinfo is not None
        assert normalized.year == 2024
        assert normalized.month == 1
        assert normalized.day == 15
    
    def test_normalize_date_from_string(self, processor):
        """Test date normalization from string."""
        date_str = "2024-01-15T10:30:00Z"
        normalized = processor.normalize_date(date_str)
        
        assert normalized.tzinfo is not None
        assert normalized.year == 2024
    
    def test_normalize_date_none(self, processor):
        """Test date normalization with None."""
        normalized = processor.normalize_date(None)
        assert normalized is not None
        assert normalized.tzinfo is not None
    
    def test_normalize_string(self, processor):
        """Test string normalization."""
        text = "  This   is   a   test  "
        normalized = processor.normalize_string(text)
        
        assert normalized == "This is a test"
    
    def test_normalize_string_truncate(self, processor):
        """Test string truncation."""
        text = "a" * 300
        normalized = processor.normalize_string(text, max_length=200)
        
        assert len(normalized) == 200
    
    def test_normalize_string_none(self, processor):
        """Test string normalization with None."""
        normalized = processor.normalize_string(None)
        assert normalized is None
    
    def test_validate_post_data_valid(self, processor):
        """Test post data validation with valid data."""
        post_data = {
            "post_id": "123",
            "channel_id": 1,
            "date": datetime.utcnow(),
            "content_type": "text",
            "views": 100,
            "likes": 10
        }
        
        is_valid, error = processor.validate_post_data(post_data)
        assert is_valid is True
        assert error is None
    
    def test_validate_post_data_missing_field(self, processor):
        """Test post data validation with missing field."""
        post_data = {
            "post_id": "123",
            "channel_id": 1,
            # Missing date
            "content_type": "text"
        }
        
        is_valid, error = processor.validate_post_data(post_data)
        assert is_valid is False
        assert "date" in error
    
    def test_validate_post_data_invalid_content_type(self, processor):
        """Test post data validation with invalid content type."""
        post_data = {
            "post_id": "123",
            "channel_id": 1,
            "date": datetime.utcnow(),
            "content_type": "invalid_type"
        }
        
        is_valid, error = processor.validate_post_data(post_data)
        assert is_valid is False
        assert "content_type" in error
    
    def test_validate_post_data_invalid_engagement_rate(self, processor):
        """Test post data validation with invalid engagement rate."""
        post_data = {
            "post_id": "123",
            "channel_id": 1,
            "date": datetime.utcnow(),
            "content_type": "text",
            "engagement_rate": 1.5  # Invalid: > 1
        }
        
        is_valid, error = processor.validate_post_data(post_data)
        assert is_valid is False
        assert "engagement_rate" in error
    
    def test_structure_post_for_table(self, processor):
        """Test structuring post for table."""
        post_data = {
            "id": 1,
            "post_id": "123",
            "channel": {
                "channel_name": "Test Channel",
                "channel_avatar_url": "https://example.com/avatar.jpg"
            },
            "date": datetime(2024, 1, 15, 10, 30, 0),
            "text": "Test post",
            "views": 1000,
            "likes": 50,
            "content_type": "text"
        }
        
        structured = processor.structure_post_for_table(post_data)
        
        assert structured["id"] == 1
        assert structured["post_id"] == "123"
        assert structured["channel"] == "Test Channel"
        assert structured["preview_text"] == "Test post"
        assert "T" in structured["date"]  # ISO format
    
    def test_process_multilingual_content_english(self, processor):
        """Test multilingual content processing - English."""
        text = "This is an English text"
        result = processor.process_multilingual_content(text)
        
        assert result["language"] == "en"
        assert result["is_multilingual"] is False
    
    def test_process_multilingual_content_russian(self, processor):
        """Test multilingual content processing - Russian."""
        text = "Это русский текст"
        result = processor.process_multilingual_content(text)
        
        assert result["language"] == "ru"
        assert result["is_multilingual"] is False
    
    def test_process_multilingual_content_mixed(self, processor):
        """Test multilingual content processing - Mixed."""
        text = "This is English и это русский"
        result = processor.process_multilingual_content(text)
        
        assert result["is_multilingual"] is True
    
    def test_prepare_for_database(self, processor):
        """Test preparing data for database."""
        post_data = {
            "post_id": 12345,  # Will be converted to string
            "channel_id": 1,
            "text": "  Test post  ",
            "date": "2024-01-15T10:30:00Z",
            "views": 1000,
            "likes": 50,
            "content_type": "text"
        }
        
        prepared = processor.prepare_for_database(post_data)
        
        assert isinstance(prepared["post_id"], str)
        assert prepared["post_id"] == "12345"
        assert prepared["text"] == "Test post"
        assert prepared["views"] == 1000
        assert prepared["date"].tzinfo is not None
    
    def test_batch_process_posts(self, processor):
        """Test batch processing of posts."""
        posts = [
            {
                "post_id": "1",
                "channel_id": 1,
                "date": datetime.utcnow(),
                "content_type": "text",
                "views": 100,
                "likes": 10
            },
            {
                "post_id": "2",
                "channel_id": 1,
                "date": datetime.utcnow(),
                "content_type": "photo",
                "views": 200,
                "likes": 20
            },
            {
                # Invalid: missing required field
                "post_id": "3",
                "channel_id": 1,
                "content_type": "text"
            }
        ]
        
        processed = processor.batch_process_posts(posts)
        
        assert len(processed) == 2  # One invalid post filtered out
        assert processed[0]["post_id"] == "1"
        assert processed[1]["post_id"] == "2"

