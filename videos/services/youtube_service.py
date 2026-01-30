import requests
from typing import Dict, List
from django.conf import settings
from django.core.cache import cache
from videos.utils.url_parser import YouTubeURLParser


class YouTubeServiceError(Exception):
    pass


class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = settings.YOUTUBE_API_BASE_URL
        self.cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 600)
        
        if not self.api_key:
            raise YouTubeServiceError("YOUTUBE_API_KEY not configured")
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
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
        if identifier_type == 'channel_id':
            return identifier
        
        cache_key = f"channel_id_{identifier_type}_{identifier}"
        cached_id = cache.get(cache_key)
        if cached_id:
            return cached_id
        
        if identifier_type == 'handle':
            params = {'part': 'id', 'forHandle': identifier}
            endpoint = 'channels'
        elif identifier_type == 'user':
            params = {'part': 'id', 'forUsername': identifier}
            endpoint = 'channels'
        elif identifier_type == 'custom_url':
            params = {'part': 'id', 'q': identifier, 'type': 'channel', 'maxResults': 1}
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
        else:
            items = response.get('items', [])
            if not items:
                raise YouTubeServiceError("Channel not found")
            channel_id = items[0]['id']['channelId']
        
        cache.set(cache_key, channel_id, self.cache_timeout)
        return channel_id
    
    def get_channel_info(self, channel_id: str) -> Dict:
        cache_key = f"channel_info_{channel_id}"
        cached_info = cache.get(cache_key)
        if cached_info:
            return cached_info
        
        params = {'part': 'snippet,contentDetails', 'id': channel_id}
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
        
        cache.set(cache_key, channel_info, self.cache_timeout)
        return channel_info
    
    def get_playlist_videos(self, playlist_id: str) -> List[Dict]:
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
                'maxResults': 50
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
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        cache.set(cache_key, all_videos, self.cache_timeout)
        return all_videos
    
    def fetch_channel_videos(self, channel_url: str, limit: int = 500, offset: int = 0) -> Dict:
        if not YouTubeURLParser.is_valid_youtube_url(channel_url):
            raise YouTubeServiceError("Invalid YouTube channel URL")
        
        identifier_data = YouTubeURLParser.extract_channel_identifier(channel_url)
        if not identifier_data:
            raise YouTubeServiceError("Could not extract channel identifier from URL")
        
        identifier, identifier_type = identifier_data
        channel_id = self.resolve_channel_id(identifier, identifier_type)
        channel_info = self.get_channel_info(channel_id)
        all_videos = self.get_playlist_videos(channel_info['uploads_playlist_id'])
        total_videos = len(all_videos)
        
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
