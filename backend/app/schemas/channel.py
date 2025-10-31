"""
Pydantic schemas for Channel model.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class ChannelBase(BaseModel):
    """Base channel schema."""
    channel_username: str = Field(..., min_length=1, max_length=255)
    channel_name: str = Field(..., min_length=1, max_length=255)
    parse_mode: str = Field(default="new_only", pattern="^(new_only|full_history)$")


class ChannelCreate(ChannelBase):
    """Schema for creating a channel."""
    pass


class ChannelUpdate(BaseModel):
    """Schema for updating a channel."""
    channel_name: Optional[str] = None
    parse_mode: Optional[str] = Field(None, pattern="^(new_only|full_history)$")
    is_active: Optional[bool] = None


class ChannelResponse(ChannelBase):
    """Schema for channel response."""
    id: int
    channel_avatar_url: Optional[str] = None
    subscribers_count: int = 0
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    last_parsed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ChannelListResponse(BaseModel):
    """Schema for list of channels."""
    channels: List[ChannelResponse]
    total: int

