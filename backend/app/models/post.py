"""
Post model for storing Telegram post data.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Post(Base):
    """Telegram post model."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String(255), nullable=False)  # Telegram post ID
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, index=True)
    
    # Content
    text = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False, index=True)
    author = Column(String(255), nullable=True)
    
    # Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    engagement_rate = Column(Float, nullable=True)
    
    # Media
    content_type = Column(String(50), nullable=False, index=True)  # text, photo, video, document, link, poll, mixed
    media_urls = Column(JSON, nullable=True)  # List of media URLs
    
    # Extracted data
    hashtags = Column(JSON, nullable=True)  # List of hashtags
    mentions = Column(JSON, nullable=True)  # List of mentions
    links = Column(JSON, nullable=True)  # List of URLs
    
    # Metadata
    parsed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    channel = relationship("Channel", back_populates="posts")
    
    # Indexes for full-text search
    __table_args__ = (
        Index('idx_post_text_search', 'text', postgresql_ops={'text': 'gin_trgm_ops'}),
        Index('idx_post_date_channel', 'date', 'channel_id'),
    )
    
    def __repr__(self):
        return f"<Post(id={self.id}, post_id={self.post_id}, channel_id={self.channel_id})>"

