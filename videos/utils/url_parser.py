import re
from typing import Optional, Tuple
from urllib.parse import urlparse


class YouTubeURLParser:
    CHANNEL_ID_PATTERN = r'channel/([a-zA-Z0-9_-]+)'
    CUSTOM_URL_PATTERN = r'c/([a-zA-Z0-9_-]+)'
    USER_PATTERN = r'user/([a-zA-Z0-9_-]+)'
    HANDLE_PATTERN = r'@([a-zA-Z0-9_-]+)'
    
    @staticmethod
    def normalize_url(url: str) -> str:
        url = url.strip()
        
        if url.startswith('@'):
            return f'https://www.youtube.com/{url}'
        
        if not url.startswith(('http://', 'https://')):
            if 'youtube.com' not in url and 'youtu.be' not in url:
                if not url.startswith('@'):
                    url = '@' + url
                return f'https://www.youtube.com/{url}'
            url = 'https://' + url
        
        if url.startswith('https://') and not url.startswith('https://www.'):
            url = url.replace('https://', 'https://www.', 1)
        elif url.startswith('http://') and not url.startswith('http://www.'):
            url = url.replace('http://', 'https://www.', 1)
        
        url = url.rstrip('/')
        return url
    
    @staticmethod
    def extract_channel_identifier(url: str) -> Optional[Tuple[str, str]]:
        normalized_url = YouTubeURLParser.normalize_url(url)
        parsed = urlparse(normalized_url)
        
        if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
            return None
        
        path = parsed.path
        
        match = re.search(YouTubeURLParser.CHANNEL_ID_PATTERN, path)
        if match:
            return (match.group(1), 'channel_id')
        
        match = re.search(YouTubeURLParser.CUSTOM_URL_PATTERN, path)
        if match:
            return (match.group(1), 'custom_url')
        
        match = re.search(YouTubeURLParser.USER_PATTERN, path)
        if match:
            return (match.group(1), 'user')
        
        match = re.search(YouTubeURLParser.HANDLE_PATTERN, path)
        if match:
            return (match.group(1), 'handle')
        
        return None
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        identifier = YouTubeURLParser.extract_channel_identifier(url)
        return identifier is not None
