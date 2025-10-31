"""
Channel model for storing Telegram channel information.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Channel(Base):
    """Telegram channel model."""
    
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(String(255), unique=True, nullable=False, index=True)
    channel_name = Column(String(255), nullable=False)
    channel_avatar_url = Column(String(512), nullable=True)
    subscribers_count = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    parse_mode = Column(String(50), default="new_only")  # "new_only" or "full_history"
    last_parsed_at = Column(DateTime, nullable=True)
    
    # Relationships
    posts = relationship("Post", back_populates="channel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Channel(id={self.id}, username={self.channel_username}, name={self.channel_name})>"

