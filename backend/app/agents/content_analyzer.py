"""
Content Analyzer Agent - анализ контента и вычисление метрик.
"""
import re
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    NLP_AVAILABLE = True
except OSError:
    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    NLP_AVAILABLE = False
    nlp = None


class ContentAnalyzerAgent:
    """Agent для анализа контента и вычисления метрик."""
    
    def __init__(self):
        """Initialize analyzer."""
        self.hashtag_pattern = re.compile(r'#\w+')
        self.mention_pattern = re.compile(r'@\w+')
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
    
    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of hashtags
        """
        if not text:
            return []
        
        hashtags = self.hashtag_pattern.findall(text)
        return list(set(hashtags))  # Remove duplicates
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract mentions from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of mentions
        """
        if not text:
            return []
        
        mentions = self.mention_pattern.findall(text)
        return list(set(mentions))  # Remove duplicates
    
    def extract_links(self, text: str) -> List[str]:
        """
        Extract URLs from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of URLs
        """
        if not text:
            return []
        
        urls = self.url_pattern.findall(text)
        # Validate URLs
        valid_urls = []
        for url in urls:
            try:
                parsed = urlparse(url)
                if parsed.scheme and parsed.netloc:
                    valid_urls.append(url)
            except Exception:
                continue
        
        return list(set(valid_urls))  # Remove duplicates
    
    def calculate_engagement_rate(self, views: int, likes: int) -> Optional[float]:
        """
        Calculate engagement rate (likes / views).
        
        Args:
            views: Number of views
            likes: Number of likes/reactions
            
        Returns:
            Engagement rate or None if views is 0
        """
        if views == 0:
            return None
        
        return round(likes / views, 6)
    
    def estimate_reading_time(self, text: str, words_per_minute: int = 200) -> int:
        """
        Estimate reading time in seconds.
        
        Args:
            text: Text to analyze
            words_per_minute: Average reading speed
            
        Returns:
            Reading time in seconds
        """
        if not text:
            return 0
        
        word_count = len(text.split())
        minutes = word_count / words_per_minute
        return int(minutes * 60)
    
    def classify_content_type(self, content_type: str, text: str, media_urls: Optional[List[str]]) -> str:
        """
        Classify content type more precisely.
        
        Args:
            content_type: Basic content type from parser
            text: Post text
            media_urls: List of media URLs
            
        Returns:
            Refined content type
        """
        if content_type == "mixed":
            return "mixed"
        
        if media_urls:
            # Check what types of media
            photo_count = sum(1 for url in media_urls if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']))
            video_count = sum(1 for url in media_urls if any(ext in url.lower() for ext in ['.mp4', '.avi', '.mov', '.webm']))
            
            if photo_count > 0 and video_count > 0:
                return "mixed"
            elif photo_count > 1:
                return "photo_gallery"
            elif video_count > 0:
                return "video"
        
        # Check for links in text
        if text and self.extract_links(text):
            return "link"
        
        if content_type == "text" and not text:
            return "media_only"
        
        return content_type
    
    def categorize_content(self, text: str) -> Optional[str]:
        """
        Categorize content by topic (basic keyword-based).
        
        Args:
            text: Text to analyze
            
        Returns:
            Content category or None
        """
        if not text:
            return None
        
        text_lower = text.lower()
        
        # News keywords
        news_keywords = ['новость', 'новости', 'news', 'breaking', 'update', 'обновление']
        if any(keyword in text_lower for keyword in news_keywords):
            return "news"
        
        # Advertisement keywords
        ad_keywords = ['реклама', 'ad', 'advertisement', 'promo', 'скидка', 'sale', 'discount']
        if any(keyword in text_lower for keyword in ad_keywords):
            return "advertisement"
        
        # Educational keywords
        edu_keywords = ['обучение', 'education', 'tutorial', 'how to', 'учебник', 'курс']
        if any(keyword in text_lower for keyword in edu_keywords):
            return "educational"
        
        # Entertainment keywords
        ent_keywords = ['развлечение', 'entertainment', 'fun', 'юмор', 'joke', 'meme']
        if any(keyword in text_lower for keyword in ent_keywords):
            return "entertainment"
        
        return None
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text using NLP.
        
        Args:
            text: Text to analyze
            max_keywords: Maximum number of keywords
            
        Returns:
            List of keywords
        """
        if not text or not NLP_AVAILABLE:
            return []
        
        try:
            doc = nlp(text)
            # Extract nouns and adjectives
            keywords = []
            for token in doc:
                if token.pos_ in ['NOUN', 'ADJ'] and not token.is_stop and not token.is_punct:
                    keywords.append(token.lemma_.lower())
            
            # Count frequency and return top keywords
            keyword_counts = {}
            for keyword in keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            
            sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            return [kw[0] for kw in sorted_keywords[:max_keywords]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def analyze_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete analysis of a post.
        
        Args:
            post_data: Raw post data from parser
            
        Returns:
            Enhanced post data with analysis
        """
        text = post_data.get("text", "")
        
        # Extract metadata
        hashtags = self.extract_hashtags(text)
        mentions = self.extract_mentions(text)
        links = self.extract_links(text)
        
        # Calculate metrics
        views = post_data.get("views", 0)
        likes = post_data.get("likes", 0)
        engagement_rate = self.calculate_engagement_rate(views, likes)
        reading_time = self.estimate_reading_time(text)
        
        # Classify content
        content_type = post_data.get("content_type", "text")
        media_urls = post_data.get("media_urls")
        refined_content_type = self.classify_content_type(content_type, text, media_urls)
        
        # Categorize content
        category = self.categorize_content(text)
        
        # Extract keywords
        keywords = self.extract_keywords(text)
        
        # Return enhanced data
        enhanced_data = {
            **post_data,
            "hashtags": hashtags if hashtags else None,
            "mentions": mentions if mentions else None,
            "links": links if links else None,
            "engagement_rate": engagement_rate,
            "reading_time": reading_time,
            "content_type": refined_content_type,
            "category": category,
            "keywords": keywords if keywords else None,
        }
        
        return enhanced_data
    
    def analyze_posts_batch(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple posts.
        
        Args:
            posts: List of raw post data
            
        Returns:
            List of enhanced post data
        """
        return [self.analyze_post(post) for post in posts]

