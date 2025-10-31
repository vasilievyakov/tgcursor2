"""
Celery tasks for channel parsing.
"""
from celery import shared_task
from app.agents.channel_parser import ChannelParserAgent
from app.core.database import SessionLocal
from app.models.channel import Channel
from app.models.post import Post
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@shared_task(name="parse_channel")
def parse_channel_task(channel_url: str, parse_mode: str = "new_only", limit: int = None):
    """
    Celery task to parse channel.
    
    Args:
        channel_url: Channel URL
        parse_mode: "new_only" or "full_history"
        limit: Maximum number of posts to parse
    """
    import asyncio
    
    async def parse():
        parser = ChannelParserAgent()
        try:
            result = await parser.parse_channel_full(channel_url, parse_mode, limit)
            
            # Save to database
            db = SessionLocal()
            try:
                # Create or update channel
                channel = db.query(Channel).filter_by(
                    channel_username=result["metadata"]["channel_username"]
                ).first()
                
                if not channel:
                    channel = Channel(**result["metadata"])
                    db.add(channel)
                else:
                    for key, value in result["metadata"].items():
                        if key != "channel_username":
                            setattr(channel, key, value)
                    channel.last_parsed_at = datetime.utcnow()
                
                db.commit()
                
                # Save posts
                for post_data in result["posts"]:
                    existing_post = db.query(Post).filter_by(
                        post_id=post_data["post_id"],
                        channel_id=channel.id
                    ).first()
                    
                    if not existing_post:
                        post_data["channel_id"] = channel.id
                        # Remove fields not in Post model
                        post_data.pop("comments", None)
                        post = Post(**post_data)
                        db.add(post)
                
                db.commit()
                logger.info(f"Successfully parsed channel {channel.channel_username}")
                
            except Exception as e:
                db.rollback()
                logger.error(f"Error saving to database: {e}")
                raise
            finally:
                db.close()
            
            await parser.disconnect()
            
        except Exception as e:
            logger.error(f"Error parsing channel {channel_url}: {e}")
            await parser.disconnect()
            raise
    
    asyncio.run(parse())


@shared_task(name="parse_channel_posts")
def parse_channel_posts_task(channel_id: int, parse_mode: str = "new_only"):
    """
    Celery task to parse new posts from existing channel.
    
    Args:
        channel_id: Channel ID in database
        parse_mode: "new_only" or "full_history"
    """
    import asyncio
    
    async def parse():
        db = SessionLocal()
        try:
            channel = db.query(Channel).filter_by(id=channel_id).first()
            if not channel:
                raise ValueError(f"Channel with id {channel_id} not found")
            
            parser = ChannelParserAgent()
            
            offset_date = None
            if parse_mode == "new_only" and channel.last_parsed_at:
                offset_date = channel.last_parsed_at
            
            posts = await parser.parse_posts(
                channel.channel_username,
                parse_mode=parse_mode,
                offset_date=offset_date
            )
            
            # Save new posts
            for post_data in posts:
                existing_post = db.query(Post).filter_by(
                    post_id=post_data["post_id"],
                    channel_id=channel.id
                ).first()
                
                if not existing_post:
                    post_data["channel_id"] = channel.id
                    post_data.pop("comments", None)
                    post = Post(**post_data)
                    db.add(post)
            
            channel.last_parsed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Successfully parsed {len(posts)} posts from channel {channel.channel_username}")
            
            await parser.disconnect()
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error parsing posts for channel {channel_id}: {e}")
            raise
        finally:
            db.close()
    
    asyncio.run(parse())

