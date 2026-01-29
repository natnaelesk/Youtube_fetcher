"""
YouTube Data API v3 service for fetching channel videos.

Handles:
- Channel ID resolution from various URL formats
- Playlist retrieval
- Pagination
- Caching
- Error handling
"""

import requests
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.core.cache import cache
from videos.utils.url_parser import YouTubeURLParser


class YouTubeServiceError(Exception):
    """Custom exception for YouTube service errors."""
    pass


class YouTubeService:
    """Service for interacting with YouTube Data API v3."""
    
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = settings.YOUTUBE_API_BASE_URL
        self.cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 600)
        
        if not self.api_key:
            raise YouTubeServiceError("YOUTUBE_API_KEY not configured")
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """
        Make a request to YouTube API with error handling.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response from API
            
        Raises:
            YouTubeServiceError: If API request fails
        """
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise YouTubeServiceError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise YouTubeServiceError(f"Invalid API response: {str(e)}")
    
    def _check_api_error(self, response: Dict) -> None:
        """
        Check API response for errors and raise appropriate exception.
        
        Args:
            response: API response dictionary
            
        Raises:
            YouTubeServiceError: If API returned an error
        """
        if 'error' in response:
            error = response['error']
            error_code = error.get('code', 'Unknown')
            error_message = error.get('message', 'Unknown error')
            
            if error_code == 403:
                raise YouTubeServiceError("API quota exceeded or access denied")
            elif error_code == 404:
                raise YouTubeServiceError("Channel not found")
            elif error_code == 400:
                raise YouTubeServiceError(f"Invalid request: {error_message}")
            else:
                raise YouTubeServiceError(f"API error: {error_message}")
    
    def resolve_channel_id(self, identifier: str, identifier_type: str) -> str:
        """
        Resolve channel identifier to channel ID.
        
        Args:
            identifier: Channel identifier (handle, custom URL, etc.)
            identifier_type: Type of identifier ('channel_id', 'custom_url', 'user', 'handle')
            
        Returns:
            Channel ID (UC...)
            
        Raises:
            YouTubeServiceError: If channel cannot be resolved
        """
        # If already a channel ID, return it
        if identifier_type == 'channel_id':
            return identifier
        
        # Check cache first
        cache_key = f"channel_id_{identifier_type}_{identifier}"
        cached_id = cache.get(cache_key)
        if cached_id:
            return cached_id
        
        # Use appropriate API endpoint based on identifier type
        if identifier_type == 'handle':
            # Use channels.list with forHandle parameter (YouTube API v3)
            params = {
                'part': 'id',
                'forHandle': identifier
            }
            endpoint = 'channels'
        elif identifier_type == 'user':
            # Use channels.list with forUsername parameter
            params = {
                'part': 'id',
                'forUsername': identifier
            }
            endpoint = 'channels'
        elif identifier_type == 'custom_url':
            # For custom URLs, we need to search
            params = {
                'part': 'id',
                'q': identifier,
                'type': 'channel',
                'maxResults': 1
            }
            endpoint = 'search'
        else:
            raise YouTubeServiceError(f"Unknown identifier type: {identifier_type}")
        
        response = self._make_request(endpoint, params)
        self._check_api_error(response)
        
        if endpoint == 'channels':
            items = response.get('items', [])
            if not items:
                raise YouTubeServiceError("Channel not found")
            channel_id = items[0]['id']
        else:  # search endpoint
            items = response.get('items', [])
            if not items:
                raise YouTubeServiceError("Channel not found")
            channel_id = items[0]['id']['channelId']
        
        # Cache the result
        cache.set(cache_key, channel_id, self.cache_timeout)
        
        return channel_id
    
    def get_channel_info(self, channel_id: str) -> Dict:
        """
        Get channel information.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Dictionary with channel title and uploads playlist ID
        """
        cache_key = f"channel_info_{channel_id}"
        cached_info = cache.get(cache_key)
        if cached_info:
            return cached_info
        
        params = {
            'part': 'snippet,contentDetails',
            'id': channel_id
        }
        
        response = self._make_request('channels', params)
        self._check_api_error(response)
        
        items = response.get('items', [])
        if not items:
            raise YouTubeServiceError("Channel not found")
        
        channel = items[0]
        channel_info = {
            'title': channel['snippet']['title'],
            'uploads_playlist_id': channel['contentDetails']['relatedPlaylists']['uploads']
        }
        
        # Cache the result
        cache.set(cache_key, channel_info, self.cache_timeout)
        
        return channel_info
    
    def get_playlist_videos(self, playlist_id: str) -> List[Dict]:
        """
        Get all videos from a playlist with pagination.
        
        Args:
            playlist_id: YouTube playlist ID
            
        Returns:
            List of video dictionaries
        """
        cache_key = f"playlist_videos_{playlist_id}"
        cached_videos = cache.get(cache_key)
        if cached_videos:
            return cached_videos
        
        all_videos = []
        next_page_token = None
        
        while True:
            params = {
                'part': 'snippet,contentDetails',
                'playlistId': playlist_id,
                'maxResults': 50  # Maximum allowed by API
            }
            
            if next_page_token:
                params['pageToken'] = next_page_token
            
            response = self._make_request('playlistItems', params)
            self._check_api_error(response)
            
            items = response.get('items', [])
            
            for item in items:
                video_data = {
                    'video_id': item['contentDetails']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'published_at': item['snippet']['publishedAt'],
                    'video_url': f"https://www.youtube.com/watch?v={item['contentDetails']['videoId']}"
                }
                all_videos.append(video_data)
            
            # Check for more pages
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        # Cache the result
        cache.set(cache_key, all_videos, self.cache_timeout)
        
        return all_videos
    
    def fetch_channel_videos(self, channel_url: str, limit: int = 500, offset: int = 0) -> Dict:
        """
        Main method to fetch videos from a channel with pagination.
        
        Args:
            channel_url: YouTube channel URL
            limit: Maximum number of videos to return (default: 500)
            offset: Offset for pagination (default: 0)
            
        Returns:
            Dictionary with channel info and videos list (paginated)
        """
        # Parse URL
        if not YouTubeURLParser.is_valid_youtube_url(channel_url):
            raise YouTubeServiceError("Invalid YouTube channel URL")
        
        identifier_data = YouTubeURLParser.extract_channel_identifier(channel_url)
        if not identifier_data:
            raise YouTubeServiceError("Could not extract channel identifier from URL")
        
        identifier, identifier_type = identifier_data
        
        # Resolve to channel ID
        channel_id = self.resolve_channel_id(identifier, identifier_type)
        
        # Get channel info
        channel_info = self.get_channel_info(channel_id)
        
        # Get videos with pagination
        all_videos = self.get_playlist_videos(channel_info['uploads_playlist_id'])
        total_videos = len(all_videos)
        
        # Apply pagination
        paginated_videos = all_videos[offset:offset + limit]
        has_more = (offset + limit) < total_videos
        next_offset = offset + limit if has_more else None
        
        return {
            'channel_title': channel_info['title'],
            'channel_id': channel_id,
            'total_videos': total_videos,
            'videos': paginated_videos,
            'has_more': has_more,
            'next_offset': next_offset
        }

