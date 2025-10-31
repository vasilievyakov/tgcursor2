"""
API routers for posts.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.core.database import get_db
from app.models.post import Post
from app.schemas.post import PostResponse, PostListResponse
from app.agents.filter_search import FilterSearchAgent

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PostListResponse)
async def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    channel_id: Optional[int] = None,
    content_type: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    keywords: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("date", regex="^(date|views|likes|engagement_rate)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """Get list of posts with filtering, search and sorting."""
    # Build filters
    filters = {}
    
    if channel_id:
        filters["channel_ids"] = [channel_id]
    
    if content_type:
        filters["content_types"] = [content_type]
    
    if date_from:
        filters["date_from"] = date_from
    
    if date_to:
        filters["date_to"] = date_to
    
    if keywords:
        filters["keywords"] = keywords.split(",")
    
    # Use FilterSearchAgent
    agent = FilterSearchAgent(db)
    result = agent.get_filtered_posts(
        filters=filters if filters else None,
        search_query=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    
    return {
        "posts": result["posts"],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"]
    }


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get post by ID."""
    post = db.query(Post).filter_by(id=post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id {post_id} not found"
        )
    
    return post

