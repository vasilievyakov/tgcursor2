"""
Tests for Channel Parser Agent.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from app.agents.channel_parser import ChannelParserAgent
from telethon.tl.types import Channel, Message, MessageMediaPhoto, MessageMediaVideo
from telethon.errors import ChannelInvalidError, ChannelPrivateError, FloodWaitError


class TestChannelParserAgent:
    """Test Channel Parser Agent."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return ChannelParserAgent()
    
    @pytest.mark.asyncio
    async def test_parse_channel_username_from_url(self, parser):
        """Test parsing channel username from URL."""
        username = await parser.parse_channel_username("https://t.me/channelname")
        assert username == "channelname"
        
        username = await parser.parse_channel_username("@channelname")
        assert username == "channelname"
        
        username = await parser.parse_channel_username("channelname")
        assert username == "channelname"
    
    @pytest.mark.asyncio
    async def test_get_channel_metadata(self, parser):
        """Test getting channel metadata."""
        # Mock Telegram client
        mock_channel = MagicMock(spec=Channel)
        mock_channel.title = "Test Channel"
        mock_channel.participants_count = 1000
        mock_channel.about = "Test description"
        mock_channel.date = datetime(2020, 1, 1)
        mock_channel.photo = None
        
        with patch.object(parser.client, 'get_entity', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_channel
            
            metadata = await parser.get_channel_metadata("test_channel")
            
            assert metadata["channel_username"] == "test_channel"
            assert metadata["channel_name"] == "Test Channel"
            assert metadata["subscribers_count"] == 1000
            assert metadata["description"] == "Test description"
    
    @pytest.mark.asyncio
    async def test_get_channel_metadata_invalid_channel(self, parser):
        """Test getting metadata for invalid channel."""
        with patch.object(parser.client, 'get_entity', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = ChannelInvalidError("Invalid channel")
            
            with pytest.raises(ValueError):
                await parser.get_channel_metadata("invalid_channel")
    
    @pytest.mark.asyncio
    async def test_get_channel_metadata_private_channel(self, parser):
        """Test getting metadata for private channel."""
        with patch.object(parser.client, 'get_entity', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = ChannelPrivateError("Private channel")
            
            with pytest.raises(ValueError):
                await parser.get_channel_metadata("private_channel")
    
    @pytest.mark.asyncio
    async def test_extract_post_data_text(self, parser):
        """Test extracting data from text post."""
        mock_message = MagicMock(spec=Message)
        mock_message.id = 12345
        mock_message.date = datetime(2024, 1, 1)
        mock_message.text = "Test post text"
        mock_message.views = 1000
        mock_message.photo = None
        mock_message.video = None
        mock_message.document = None
        mock_message.entities = None
        mock_message.reactions = None
        
        post_data = await parser._extract_post_data(mock_message, "test_channel")
        
        assert post_data["post_id"] == "12345"
        assert post_data["text"] == "Test post text"
        assert post_data["content_type"] == "text"
        assert post_data["views"] == 1000
        assert post_data["likes"] == 0
    
    @pytest.mark.asyncio
    async def test_extract_post_data_photo(self, parser):
        """Test extracting data from photo post."""
        mock_message = MagicMock(spec=Message)
        mock_message.id = 12345
        mock_message.date = datetime(2024, 1, 1)
        mock_message.text = None
        mock_message.views = 1000
        mock_message.photo = MagicMock()
        mock_message.video = None
        mock_message.document = None
        mock_message.entities = None
        mock_message.reactions = None
        
        post_data = await parser._extract_post_data(mock_message, "test_channel")
        
        assert post_data["content_type"] == "photo"
        assert len(post_data["media_urls"]) > 0
    
    @pytest.mark.asyncio
    async def test_parse_channel_full(self, parser):
        """Test parsing full channel."""
        mock_channel = MagicMock(spec=Channel)
        mock_channel.title = "Test Channel"
        mock_channel.participants_count = 1000
        mock_channel.about = None
        mock_channel.date = datetime(2020, 1, 1)
        mock_channel.photo = None
        
        mock_message = MagicMock(spec=Message)
        mock_message.id = 1
        mock_message.date = datetime(2024, 1, 1)
        mock_message.text = "Test post"
        mock_message.views = 100
        mock_message.photo = None
        mock_message.video = None
        mock_message.document = None
        mock_message.entities = None
        mock_message.reactions = None
        
        with patch.object(parser.client, 'get_entity', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_channel
            
            with patch.object(parser.client, 'iter_messages', new_callable=AsyncMock) as mock_iter:
                async def mock_iter_messages(*args, **kwargs):
                    yield mock_message
                
                mock_iter.return_value = mock_iter_messages()
                
                result = await parser.parse_channel_full("https://t.me/test_channel")
                
                assert "metadata" in result
                assert "posts" in result
                assert len(result["posts"]) == 1

