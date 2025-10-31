"""
Channel Parser Agent - парсинг Telegram каналов.
"""
import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Channel, Message
from telethon.errors import FloodWaitError, ChannelInvalidError, ChannelPrivateError
from app.core.config import settings

logger = logging.getLogger(__name__)


class ChannelParserAgent:
    """Agent для парсинга Telegram каналов."""
    
    def __init__(self):
        """Initialize Telegram client."""
        self.client = TelegramClient(
            'tgcursor2_session',
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )
        self._connected = False
    
    async def connect(self):
        """Connect to Telegram."""
        if not self._connected:
            await self.client.start()
            self._connected = True
            logger.info("Connected to Telegram")
    
    async def disconnect(self):
        """Disconnect from Telegram."""
        if self._connected:
            await self.client.disconnect()
            self._connected = False
            logger.info("Disconnected from Telegram")
    
    async def parse_channel_username(self, channel_url: str) -> str:
        """
        Extract channel username from URL.
        
        Args:
            channel_url: URL like https://t.me/channelname
            
        Returns:
            Channel username without @
        """
        if channel_url.startswith("https://t.me/"):
            username = channel_url.replace("https://t.me/", "").strip()
            if username.startswith("@"):
                username = username[1:]
            return username
        elif channel_url.startswith("@"):
            return channel_url[1:]
        else:
            return channel_url
    
    async def get_channel_metadata(self, channel_username: str) -> Dict[str, Any]:
        """
        Get channel metadata.
        
        Args:
            channel_username: Channel username without @
            
        Returns:
            Dictionary with channel metadata
        """
        await self.connect()
        
        try:
            entity = await self.client.get_entity(channel_username)
            
            if not isinstance(entity, Channel):
                raise ValueError(f"{channel_username} is not a channel")
            
            metadata = {
                "channel_username": channel_username,
                "channel_name": entity.title or channel_username,
                "channel_avatar_url": None,
                "subscribers_count": getattr(entity, 'participants_count', 0) or 0,
                "description": getattr(entity, 'about', None) or None,
                "created_at": getattr(entity, 'date', None),
            }
            
            # Try to get avatar URL
            if entity.photo:
                try:
                    photo = await self.client.download_profile_photo(entity, file=bytes)
                    # In production, upload to cloud storage and get URL
                    metadata["channel_avatar_url"] = f"https://t.me/{channel_username}/1"
                except Exception as e:
                    logger.warning(f"Could not get avatar for {channel_username}: {e}")
            
            return metadata
            
        except ChannelInvalidError:
            raise ValueError(f"Channel {channel_username} is invalid or does not exist")
        except ChannelPrivateError:
            raise ValueError(f"Channel {channel_username} is private (not supported in MVP)")
        except Exception as e:
            logger.error(f"Error getting metadata for {channel_username}: {e}")
            raise
    
    async def parse_posts(
        self,
        channel_username: str,
        parse_mode: str = "new_only",
        limit: Optional[int] = None,
        offset_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Parse posts from channel.
        
        Args:
            channel_username: Channel username without @
            parse_mode: "new_only" or "full_history"
            limit: Maximum number of posts to parse
            offset_date: For "new_only" mode, parse posts after this date
            
        Returns:
            List of post dictionaries
        """
        await self.connect()
        
        try:
            entity = await self.client.get_entity(channel_username)
            
            if not isinstance(entity, Channel):
                raise ValueError(f"{channel_username} is not a channel")
            
            posts = []
            max_id = 0
            
            async for message in self.client.iter_messages(entity, limit=limit, offset_date=offset_date):
                if message is None:
                    break
                
                try:
                    post_data = await self._extract_post_data(message, channel_username)
                    posts.append(post_data)
                    
                    # Rate limiting - wait if needed
                    await asyncio.sleep(0.5)  # Basic rate limiting
                    
                except FloodWaitError as e:
                    logger.warning(f"Rate limit hit, waiting {e.seconds} seconds")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    logger.error(f"Error extracting post {message.id}: {e}")
                    continue
            
            logger.info(f"Parsed {len(posts)} posts from {channel_username}")
            return posts
            
        except Exception as e:
            logger.error(f"Error parsing posts from {channel_username}: {e}")
            raise
    
    async def _extract_post_data(self, message: Message, channel_username: str) -> Dict[str, Any]:
        """
        Extract data from Telegram message.
        
        Args:
            message: Telegram message object
            channel_username: Channel username
            
        Returns:
            Dictionary with post data
        """
        # Determine content type
        content_type = "text"
        media_urls = []
        
        if message.photo:
            content_type = "photo"
            try:
                # Download media URL
                media_urls.append(f"https://t.me/{channel_username}/{message.id}")
            except Exception as e:
                logger.warning(f"Could not get photo URL: {e}")
        
        elif message.video:
            content_type = "video"
            media_urls.append(f"https://t.me/{channel_username}/{message.id}")
        
        elif message.document:
            content_type = "document"
            media_urls.append(f"https://t.me/{channel_username}/{message.id}")
        
        elif message.entities:
            # Check for links
            for entity in message.entities:
                if hasattr(entity, 'url'):
                    content_type = "link"
                    break
        
        if message.photo and message.text:
            content_type = "mixed"
        
        # Extract basic data
        post_data = {
            "post_id": str(message.id),
            "date": message.date if message.date else datetime.utcnow(),
            "text": message.text or message.raw_text or "",
            "author": None,  # Channels don't have authors
            "content_type": content_type,
            "media_urls": media_urls if media_urls else None,
            "views": message.views or 0,
            "likes": 0,  # Reactions need special handling
            "comments": None,  # Comments not available in MVP
        }
        
        # Extract reactions if available
        if hasattr(message, 'reactions') and message.reactions:
            total_reactions = sum(
                reaction.count for reaction in message.reactions.results
            )
            post_data["likes"] = total_reactions
        
        return post_data
    
    async def parse_channel_full(
        self,
        channel_url: str,
        parse_mode: str = "new_only",
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Parse channel metadata and posts.
        
        Args:
            channel_url: Channel URL
            parse_mode: "new_only" or "full_history"
            limit: Maximum number of posts to parse
            
        Returns:
            Dictionary with channel metadata and posts
        """
        channel_username = await self.parse_channel_username(channel_url)
        
        metadata = await self.get_channel_metadata(channel_username)
        posts = await self.parse_posts(channel_username, parse_mode=parse_mode, limit=limit)
        
        return {
            "metadata": metadata,
            "posts": posts
        }

