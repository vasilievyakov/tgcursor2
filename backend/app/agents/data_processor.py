"""
Data Processor Agent - нормализация и структурирование данных.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dateutil import parser as date_parser
import pytz

logger = logging.getLogger(__name__)


class DataProcessorAgent:
    """Agent для обработки и нормализации данных."""
    
    def __init__(self):
        """Initialize processor."""
        self.utc_timezone = pytz.UTC
    
    def normalize_date(self, date_input: Any) -> datetime:
        """
        Normalize date to ISO 8601 format (UTC).
        
        Args:
            date_input: Date in various formats
            
        Returns:
            Normalized datetime object
        """
        if date_input is None:
            return datetime.utcnow().replace(tzinfo=self.utc_timezone)
        
        if isinstance(date_input, datetime):
            # Ensure timezone awareness
            if date_input.tzinfo is None:
                date_input = date_input.replace(tzinfo=self.utc_timezone)
            else:
                date_input = date_input.astimezone(self.utc_timezone)
            return date_input
        
        if isinstance(date_input, str):
            try:
                parsed_date = date_parser.parse(date_input)
                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=self.utc_timezone)
                else:
                    parsed_date = parsed_date.astimezone(self.utc_timezone)
                return parsed_date
            except Exception as e:
                logger.warning(f"Could not parse date '{date_input}': {e}")
                return datetime.utcnow().replace(tzinfo=self.utc_timezone)
        
        # Fallback
        return datetime.utcnow().replace(tzinfo=self.utc_timezone)
    
    def normalize_string(self, text: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
        """
        Normalize string - strip whitespace, handle None.
        
        Args:
            text: Text to normalize
            max_length: Maximum length (truncate if longer)
            
        Returns:
            Normalized string or None
        """
        if text is None:
            return None
        
        # Strip whitespace
        normalized = text.strip()
        
        # Remove multiple spaces
        normalized = " ".join(normalized.split())
        
        # Truncate if needed
        if max_length and len(normalized) > max_length:
            normalized = normalized[:max_length]
            logger.warning(f"Text truncated to {max_length} characters")
        
        return normalized if normalized else None
    
    def validate_post_data(self, post_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate post data before saving.
        
        Args:
            post_data: Post data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ["post_id", "channel_id", "date", "content_type"]
        for field in required_fields:
            if field not in post_data or post_data[field] is None:
                return False, f"Missing required field: {field}"
        
        # Validate content_type
        valid_content_types = ["text", "photo", "video", "document", "link", "poll", "mixed"]
        if post_data["content_type"] not in valid_content_types:
            return False, f"Invalid content_type: {post_data['content_type']}"
        
        # Validate numeric fields
        numeric_fields = ["views", "likes"]
        for field in numeric_fields:
            if field in post_data and post_data[field] is not None:
                if not isinstance(post_data[field], int) or post_data[field] < 0:
                    return False, f"Invalid {field}: must be non-negative integer"
        
        # Validate engagement_rate
        if "engagement_rate" in post_data and post_data["engagement_rate"] is not None:
            rate = post_data["engagement_rate"]
            if not isinstance(rate, float) or rate < 0 or rate > 1:
                return False, "Invalid engagement_rate: must be between 0 and 1"
        
        # Validate JSON fields
        json_fields = ["media_urls", "hashtags", "mentions", "links"]
        for field in json_fields:
            if field in post_data and post_data[field] is not None:
                if not isinstance(post_data[field], list):
                    return False, f"Invalid {field}: must be a list"
        
        return True, None
    
    def validate_channel_data(self, channel_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate channel data before saving.
        
        Args:
            channel_data: Channel data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ["channel_username", "channel_name"]
        for field in required_fields:
            if field not in channel_data or not channel_data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate parse_mode
        if "parse_mode" in channel_data:
            valid_modes = ["new_only", "full_history"]
            if channel_data["parse_mode"] not in valid_modes:
                return False, f"Invalid parse_mode: {channel_data['parse_mode']}"
        
        # Validate subscribers_count
        if "subscribers_count" in channel_data and channel_data["subscribers_count"] is not None:
            if not isinstance(channel_data["subscribers_count"], int) or channel_data["subscribers_count"] < 0:
                return False, "Invalid subscribers_count: must be non-negative integer"
        
        return True, None
    
    def structure_post_for_table(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure post data for table display.
        
        Args:
            post_data: Raw post data
            
        Returns:
            Structured post data for table
        """
        # Normalize date
        normalized_date = self.normalize_date(post_data.get("date"))
        
        # Normalize text
        normalized_text = self.normalize_string(post_data.get("text"))
        
        # Truncate text for preview
        preview_text = normalized_text[:200] + "..." if normalized_text and len(normalized_text) > 200 else normalized_text
        
        # Structure data
        structured = {
            "id": post_data.get("id"),
            "post_id": post_data.get("post_id"),
            "channel": post_data.get("channel", {}).get("channel_name") if isinstance(post_data.get("channel"), dict) else None,
            "channel_avatar": post_data.get("channel", {}).get("channel_avatar_url") if isinstance(post_data.get("channel"), dict) else None,
            "date": normalized_date.isoformat(),
            "text": normalized_text,
            "preview_text": preview_text,
            "author": post_data.get("author"),
            "views": post_data.get("views", 0),
            "likes": post_data.get("likes", 0),
            "engagement_rate": post_data.get("engagement_rate"),
            "content_type": post_data.get("content_type", "text"),
            "media_urls": post_data.get("media_urls", []),
            "hashtags": post_data.get("hashtags", []),
            "mentions": post_data.get("mentions", []),
            "links": post_data.get("links", []),
            "parsed_at": self.normalize_date(post_data.get("parsed_at")).isoformat() if post_data.get("parsed_at") else None,
        }
        
        return structured
    
    def structure_channel_for_table(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure channel data for table display.
        
        Args:
            channel_data: Raw channel data
            
        Returns:
            Structured channel data for table
        """
        structured = {
            "id": channel_data.get("id"),
            "channel_username": channel_data.get("channel_username"),
            "channel_name": channel_data.get("channel_name"),
            "channel_avatar_url": channel_data.get("channel_avatar_url"),
            "subscribers_count": channel_data.get("subscribers_count", 0),
            "description": self.normalize_string(channel_data.get("description"), max_length=500),
            "is_active": channel_data.get("is_active", True),
            "parse_mode": channel_data.get("parse_mode", "new_only"),
            "last_parsed_at": self.normalize_date(channel_data.get("last_parsed_at")).isoformat() if channel_data.get("last_parsed_at") else None,
            "created_at": self.normalize_date(channel_data.get("created_at")).isoformat() if channel_data.get("created_at") else None,
        }
        
        return structured
    
    def process_multilingual_content(self, text: Optional[str]) -> Dict[str, Any]:
        """
        Detect and process multilingual content.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with language info
        """
        if not text:
            return {"language": None, "is_multilingual": False}
        
        # Simple language detection (basic implementation)
        # In production, use langdetect or similar library
        
        cyrillic_chars = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        latin_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)
        
        if cyrillic_chars > latin_chars:
            language = "ru"
        elif latin_chars > 0:
            language = "en"
        else:
            language = "unknown"
        
        # Check if multilingual
        is_multilingual = cyrillic_chars > 0 and latin_chars > 0
        
        return {
            "language": language,
            "is_multilingual": is_multilingual,
            "cyrillic_ratio": cyrillic_chars / len(text) if text else 0,
            "latin_ratio": latin_chars / len(text) if text else 0,
        }
    
    def prepare_for_database(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare post data for database insertion.
        
        Args:
            post_data: Post data dictionary
            
        Returns:
            Prepared data dictionary
        """
        prepared = {}
        
        # Copy and normalize fields
        prepared["post_id"] = str(post_data.get("post_id"))
        prepared["channel_id"] = post_data.get("channel_id")
        prepared["text"] = self.normalize_string(post_data.get("text"))
        prepared["date"] = self.normalize_date(post_data.get("date"))
        prepared["author"] = self.normalize_string(post_data.get("author"), max_length=255)
        prepared["views"] = post_data.get("views", 0) or 0
        prepared["likes"] = post_data.get("likes", 0) or 0
        prepared["engagement_rate"] = post_data.get("engagement_rate")
        prepared["content_type"] = post_data.get("content_type", "text")
        prepared["media_urls"] = post_data.get("media_urls")
        prepared["hashtags"] = post_data.get("hashtags")
        prepared["mentions"] = post_data.get("mentions")
        prepared["links"] = post_data.get("links")
        
        # Set parsed_at if not present
        if "parsed_at" not in prepared or prepared["parsed_at"] is None:
            prepared["parsed_at"] = datetime.utcnow().replace(tzinfo=self.utc_timezone)
        
        return prepared
    
    def batch_process_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple posts.
        
        Args:
            posts: List of post data dictionaries
            
        Returns:
            List of processed post data
        """
        processed = []
        errors = []
        
        for post in posts:
            try:
                # Validate
                is_valid, error = self.validate_post_data(post)
                if not is_valid:
                    errors.append({"post_id": post.get("post_id"), "error": error})
                    continue
                
                # Prepare for database
                prepared = self.prepare_for_database(post)
                processed.append(prepared)
                
            except Exception as e:
                errors.append({"post_id": post.get("post_id"), "error": str(e)})
                logger.error(f"Error processing post {post.get('post_id')}: {e}")
        
        if errors:
            logger.warning(f"Processed {len(processed)} posts, {len(errors)} errors")
        
        return processed

