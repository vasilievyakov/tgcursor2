"""
Tests for Export Agent.
"""
import pytest
from datetime import datetime
from app.agents.export import ExportAgent


class TestExportAgent:
    """Test Export Agent."""
    
    @pytest.fixture
    def exporter(self):
        """Create exporter instance."""
        return ExportAgent()
    
    @pytest.fixture
    def sample_posts(self):
        """Create sample post data."""
        return [
            {
                "id": 1,
                "post_id": "123",
                "channel": "Test Channel",
                "date": datetime(2024, 1, 15, 10, 30, 0),
                "text": "Test post with #hashtag",
                "author": "user1",
                "views": 1000,
                "likes": 50,
                "engagement_rate": 0.05,
                "content_type": "text",
                "hashtags": ["#hashtag"],
                "mentions": ["@user"],
                "links": ["https://example.com"]
            },
            {
                "id": 2,
                "post_id": "124",
                "channel": "Test Channel",
                "date": datetime(2024, 1, 16, 11, 0, 0),
                "text": "Another post",
                "author": None,
                "views": 2000,
                "likes": 100,
                "engagement_rate": 0.05,
                "content_type": "photo",
                "hashtags": [],
                "mentions": [],
                "links": []
            }
        ]
    
    def test_export_to_csv(self, exporter, sample_posts):
        """Test CSV export."""
        csv_bytes = exporter.export_to_csv(sample_posts)
        
        assert csv_bytes is not None
        assert len(csv_bytes) > 0
        
        # Decode and check content
        csv_str = csv_bytes.decode('utf-8-sig')
        assert "id" in csv_str
        assert "post_id" in csv_str
        assert "Test Channel" in csv_str
    
    def test_export_to_csv_with_columns(self, exporter, sample_posts):
        """Test CSV export with specific columns."""
        columns = ["id", "post_id", "text", "views"]
        csv_bytes = exporter.export_to_csv(sample_posts, columns=columns)
        
        csv_str = csv_bytes.decode('utf-8-sig')
        assert "id" in csv_str
        assert "post_id" in csv_str
        assert "text" in csv_str
        assert "views" in csv_str
        assert "channel" not in csv_str  # Should not be in output
    
    def test_export_to_csv_empty(self, exporter):
        """Test CSV export with empty data."""
        csv_bytes = exporter.export_to_csv([])
        assert csv_bytes == b""
    
    def test_export_to_excel(self, exporter, sample_posts):
        """Test Excel export."""
        excel_bytes = exporter.export_to_excel(sample_posts)
        
        assert excel_bytes is not None
        assert len(excel_bytes) > 0
        
        # Check that it's a valid Excel file (starts with PK signature)
        assert excel_bytes[:2] == b'PK'
    
    def test_export_to_excel_with_columns(self, exporter, sample_posts):
        """Test Excel export with specific columns."""
        columns = ["id", "post_id", "text"]
        excel_bytes = exporter.export_to_excel(sample_posts, columns=columns)
        
        assert excel_bytes is not None
        assert len(excel_bytes) > 0
    
    def test_export_to_google_sheets_format(self, exporter, sample_posts):
        """Test Google Sheets format export."""
        rows = exporter.export_to_google_sheets_format(sample_posts)
        
        assert len(rows) == 3  # Header + 2 data rows
        assert len(rows[0]) > 0  # Header row
        assert rows[0][0] == "id"  # First column
    
    def test_prepare_posts_for_export(self, exporter):
        """Test preparing posts for export."""
        from app.models.post import Post
        from app.models.channel import Channel
        
        # Create mock post object
        channel = Channel(
            channel_username="test",
            channel_name="Test Channel"
        )
        
        post = Post(
            post_id="123",
            channel_id=1,
            text="Test",
            date=datetime.utcnow(),
            content_type="text",
            views=100,
            likes=10
        )
        post.channel = channel
        
        export_data = exporter.prepare_posts_for_export([post])
        
        assert len(export_data) == 1
        assert export_data[0]["post_id"] == "123"
        assert export_data[0]["channel"] == "Test Channel"
        assert export_data[0]["views"] == 100

