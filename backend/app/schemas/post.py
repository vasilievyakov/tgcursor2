"""
Pydantic schemas for Post model.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """Base post schema."""
    post_id: str
    text: Optional[str] = None
    date: datetime
    author: Optional[str] = None
    views: int = 0
    likes: int = 0
    content_type: str = Field(..., pattern="^(text|photo|video|document|link|poll|mixed)$")


class PostCreate(PostBase):
    """Schema for creating a post."""
    channel_id: int
    media_urls: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    links: Optional[List[str]] = None


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    views: Optional[int] = None
    likes: Optional[int] = None
    engagement_rate: Optional[float] = None


class PostResponse(PostBase):
    """Schema for post response."""
    id: int
    channel_id: int
    engagement_rate: Optional[float] = None
    media_urls: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    links: Optional[List[str]] = None
    parsed_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """Schema for list of posts."""
    posts: List[PostResponse]
    total: int
    page: int
    page_size: int

