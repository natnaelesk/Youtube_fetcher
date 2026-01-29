"""
URL parser utility for extracting channel identifiers from various YouTube URL formats.

Handles:
- Channel ID format: https://www.youtube.com/channel/UC...
- Custom URL format: https://www.youtube.com/c/ChannelName
- User format: https://www.youtube.com/user/username
- @handle format: https://www.youtube.com/@handle
- Short format: youtube.com/@handle
"""

import re
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs


class YouTubeURLParser:
    """Parse and normalize YouTube channel URLs."""
    
    # Patterns for different YouTube URL formats
    CHANNEL_ID_PATTERN = r'channel/([a-zA-Z0-9_-]+)'
    CUSTOM_URL_PATTERN = r'c/([a-zA-Z0-9_-]+)'
    USER_PATTERN = r'user/([a-zA-Z0-9_-]+)'
    HANDLE_PATTERN = r'@([a-zA-Z0-9_-]+)'
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize YouTube URL to a standard format.
        
        Args:
            url: Raw YouTube URL string
            
        Returns:
            Normalized URL string
        """
        url = url.strip()
        
        # Handle @handle format (just the handle)
        if url.startswith('@'):
            return f'https://www.youtube.com/{url}'
        
        # Add protocol if missing (but not for just handles)
        if not url.startswith(('http://', 'https://')):
            # If it doesn't contain youtube.com, assume it's a handle
            if 'youtube.com' not in url and 'youtu.be' not in url:
                if not url.startswith('@'):
                    url = '@' + url
                return f'https://www.youtube.com/{url}'
            url = 'https://' + url
        
        # Normalize www
        if url.startswith('https://') and not url.startswith('https://www.'):
            url = url.replace('https://', 'https://www.', 1)
        elif url.startswith('http://') and not url.startswith('http://www.'):
            url = url.replace('http://', 'https://www.', 1)
        
        # Remove trailing slashes
        url = url.rstrip('/')
        
        return url
    
    @staticmethod
    def extract_channel_identifier(url: str) -> Optional[Tuple[str, str]]:
        """
        Extract channel identifier and type from URL.
        
        Args:
            url: YouTube channel URL
            
        Returns:
            Tuple of (identifier, type) or None if invalid
            Types: 'channel_id', 'custom_url', 'user', 'handle'
        """
        normalized_url = YouTubeURLParser.normalize_url(url)
        parsed = urlparse(normalized_url)
        
        # Must be a YouTube domain
        if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
            return None
        
        path = parsed.path
        
        # Check for channel ID format: /channel/UC...
        match = re.search(YouTubeURLParser.CHANNEL_ID_PATTERN, path)
        if match:
            return (match.group(1), 'channel_id')
        
        # Check for custom URL format: /c/ChannelName
        match = re.search(YouTubeURLParser.CUSTOM_URL_PATTERN, path)
        if match:
            return (match.group(1), 'custom_url')
        
        # Check for user format: /user/username
        match = re.search(YouTubeURLParser.USER_PATTERN, path)
        if match:
            return (match.group(1), 'user')
        
        # Check for handle format: /@handle
        match = re.search(YouTubeURLParser.HANDLE_PATTERN, path)
        if match:
            return (match.group(1), 'handle')
        
        return None
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """
        Validate if URL is a YouTube channel URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid YouTube channel URL, False otherwise
        """
        identifier = YouTubeURLParser.extract_channel_identifier(url)
        return identifier is not None

