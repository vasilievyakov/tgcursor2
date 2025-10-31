"""
Filter & Search Agent - фильтрация, поиск и сортировка данных.
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Query
from sqlalchemy import or_, and_, func, String
from app.models.post import Post
from app.models.channel import Channel

logger = logging.getLogger(__name__)


class FilterSearchAgent:
    """Agent для фильтрации, поиска и сортировки."""
    
    def __init__(self, db_session):
        """Initialize agent with database session."""
        self.db = db_session
    
    def filter_posts(
        self,
        query: Query,
        filters: Dict[str, Any]
    ) -> Query:
        """
        Apply filters to posts query.
        
        Args:
            query: SQLAlchemy query object
            filters: Dictionary with filter parameters
            
        Returns:
            Filtered query
        """
        # Filter by date range
        if "date_from" in filters and filters["date_from"]:
            query = query.filter(Post.date >= filters["date_from"])
        
        if "date_to" in filters and filters["date_to"]:
            query = query.filter(Post.date <= filters["date_to"])
        
        # Filter by channel IDs
        if "channel_ids" in filters and filters["channel_ids"]:
            query = query.filter(Post.channel_id.in_(filters["channel_ids"]))
        
        # Filter by content type
        if "content_types" in filters and filters["content_types"]:
            query = query.filter(Post.content_type.in_(filters["content_types"]))
        
        # Filter by keywords (full-text search in text)
        if "keywords" in filters and filters["keywords"]:
            keyword_conditions = []
            for keyword in filters["keywords"]:
                keyword_conditions.append(Post.text.ilike(f"%{keyword}%"))
            query = query.filter(or_(*keyword_conditions))
        
        # Filter by hashtags
        if "hashtags" in filters and filters["hashtags"]:
            # PostgreSQL JSONB query
            hashtag_conditions = []
            for hashtag in filters["hashtags"]:
                hashtag_conditions.append(Post.hashtags.contains([hashtag]))
            query = query.filter(or_(*hashtag_conditions))
        
        # Filter by views range
        if "views_min" in filters and filters["views_min"] is not None:
            query = query.filter(Post.views >= filters["views_min"])
        
        if "views_max" in filters and filters["views_max"] is not None:
            query = query.filter(Post.views <= filters["views_max"])
        
        # Filter by likes range
        if "likes_min" in filters and filters["likes_min"] is not None:
            query = query.filter(Post.likes >= filters["likes_min"])
        
        if "likes_max" in filters and filters["likes_max"] is not None:
            query = query.filter(Post.likes <= filters["likes_max"])
        
        # Filter by engagement rate range
        if "engagement_rate_min" in filters and filters["engagement_rate_min"] is not None:
            query = query.filter(Post.engagement_rate >= filters["engagement_rate_min"])
        
        if "engagement_rate_max" in filters and filters["engagement_rate_max"] is not None:
            query = query.filter(Post.engagement_rate <= filters["engagement_rate_max"])
        
        return query
    
    def search_posts(
        self,
        query: Query,
        search_query: str
    ) -> Query:
        """
        Full-text search in posts.
        
        Args:
            query: SQLAlchemy query object
            search_query: Search string
            
        Returns:
            Query with search applied
        """
        if not search_query:
            return query
        
        # Split search query into words
        words = search_query.strip().split()
        
        if not words:
            return query
        
        # Create conditions for each word
        search_conditions = []
        for word in words:
            word_pattern = f"%{word}%"
            conditions = [Post.text.ilike(word_pattern)]
            
            # Search in hashtags (JSONB array)
            if Post.hashtags is not None:
                conditions.append(func.cast(Post.hashtags, String).ilike(word_pattern))
            
            # Search in mentions (JSONB array)
            if Post.mentions is not None:
                conditions.append(func.cast(Post.mentions, String).ilike(word_pattern))
            
            search_conditions.append(or_(*conditions))
        
        # All words must match
        query = query.filter(and_(*search_conditions))
        
        return query
    
    def sort_posts(
        self,
        query: Query,
        sort_by: str = "date",
        sort_order: str = "desc"
    ) -> Query:
        """
        Sort posts.
        
        Args:
            query: SQLAlchemy query object
            sort_by: Field to sort by (date, views, likes, engagement_rate)
            sort_order: Sort order (asc, desc)
            
        Returns:
            Sorted query
        """
        valid_sort_fields = {
            "date": Post.date,
            "views": Post.views,
            "likes": Post.likes,
            "engagement_rate": Post.engagement_rate,
        }
        
        if sort_by not in valid_sort_fields:
            sort_by = "date"
        
        sort_field = valid_sort_fields[sort_by]
        
        if sort_order.lower() == "asc":
            query = query.order_by(sort_field.asc())
        else:
            query = query.order_by(sort_field.desc())
        
        # Secondary sort by date (if not primary)
        if sort_by != "date":
            query = query.order_by(Post.date.desc())
        
        return query
    
    def get_filtered_posts(
        self,
        filters: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 50
    ) -> Dict[str, Any]:
        """
        Get filtered, searched and sorted posts with pagination.
        
        Args:
            filters: Dictionary with filter parameters
            search_query: Full-text search string
            sort_by: Field to sort by
            sort_order: Sort order (asc, desc)
            page: Page number (1-based)
            page_size: Number of items per page
            
        Returns:
            Dictionary with posts and metadata
        """
        # Start with base query
        query = self.db.query(Post).join(Channel)
        
        # Apply filters
        if filters:
            query = self.filter_posts(query, filters)
        
        # Apply search
        if search_query:
            query = self.search_posts(query, search_query)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self.sort_posts(query, sort_by, sort_order)
        
        # Apply pagination
        offset = (page - 1) * page_size
        posts = query.offset(offset).limit(page_size).all()
        
        return {
            "posts": posts,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    
    def get_channels_list(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Channel]:
        """
        Get list of channels with optional filters.
        
        Args:
            filters: Dictionary with filter parameters
            
        Returns:
            List of channels
        """
        query = self.db.query(Channel)
        
        if filters:
            # Filter by active status
            if "is_active" in filters and filters["is_active"] is not None:
                query = query.filter(Channel.is_active == filters["is_active"])
            
            # Search by name or username
            if "search" in filters and filters["search"]:
                search_pattern = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Channel.channel_name.ilike(search_pattern),
                        Channel.channel_username.ilike(search_pattern),
                    )
                )
        
        return query.order_by(Channel.channel_name.asc()).all()

