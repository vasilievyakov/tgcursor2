"""
API routers for channels.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate, ChannelListResponse
from app.core.tasks import parse_channel_task
from app.core.config import settings

router = APIRouter(prefix="/channels", tags=["channels"])


@router.post("/", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    channel_data: ChannelCreate,
    db: Session = Depends(get_db)
):
    """Create a new channel and start parsing."""
    # Check if channel already exists
    existing = db.query(Channel).filter_by(
        channel_username=channel_data.channel_username
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Channel {channel_data.channel_username} already exists"
        )
    
    # Create channel
    channel = Channel(**channel_data.dict())
    db.add(channel)
    db.commit()
    db.refresh(channel)
    
    # Start parsing task
    parse_channel_task.delay(
        f"https://t.me/{channel_data.channel_username}",
        channel_data.parse_mode
    )
    
    return channel


@router.get("/", response_model=ChannelListResponse)
async def list_channels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of channels."""
    channels = db.query(Channel).offset(skip).limit(limit).all()
    total = db.query(Channel).count()
    
    return {
        "channels": channels,
        "total": total
    }


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):
    """Get channel by ID."""
    channel = db.query(Channel).filter_by(id=channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel with id {channel_id} not found"
        )
    
    return channel


@router.patch("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    channel_update: ChannelUpdate,
    db: Session = Depends(get_db)
):
    """Update channel."""
    channel = db.query(Channel).filter_by(id=channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel with id {channel_id} not found"
        )
    
    # Update fields
    update_data = channel_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(channel, field, value)
    
    db.commit()
    db.refresh(channel)
    
    return channel


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):
    """Delete channel."""
    channel = db.query(Channel).filter_by(id=channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel with id {channel_id} not found"
        )
    
    db.delete(channel)
    db.commit()
    
    return None


@router.post("/{channel_id}/parse", status_code=status.HTTP_202_ACCEPTED)
async def trigger_parse(
    channel_id: int,
    parse_mode: str = "new_only",
    db: Session = Depends(get_db)
):
    """Trigger parsing for a channel."""
    from app.core.tasks import parse_channel_posts_task
    
    channel = db.query(Channel).filter_by(id=channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel with id {channel_id} not found"
        )
    
    # Start parsing task
    parse_channel_posts_task.delay(channel_id, parse_mode)
    
    return {"message": "Parsing started", "channel_id": channel_id}

