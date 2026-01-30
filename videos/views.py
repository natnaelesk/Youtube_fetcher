from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from videos.serializers import (
    ChannelVideosRequestSerializer,
    ChannelVideosResponseSerializer
)
from videos.services.youtube_service import YouTubeService, YouTubeServiceError


def custom_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': str(exc),
            'details': response.data
        }
        response.data = custom_response_data
    
    return response


@api_view(['POST'])
def fetch_channel_videos(request):
    serializer = ChannelVideosRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                'error': True,
                'message': 'Invalid request data. Please provide a valid YouTube channel URL.',
                'details': serializer.errors,
                'help': 'Accepted formats: @handle, www.youtube.com/@handle, https://www.youtube.com/@handle, or full channel URL'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    channel_url = serializer.validated_data['channel_url']
    limit = request.data.get('limit', 500)
    offset = request.data.get('offset', 0)
    
    if limit > 1000:
        limit = 1000
    if limit < 1:
        limit = 500
    
    try:
        youtube_service = YouTubeService()
        result = youtube_service.fetch_channel_videos(channel_url, limit=limit, offset=offset)
        response_serializer = ChannelVideosResponseSerializer(result)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    except YouTubeServiceError as e:
        error_message = str(e)
        if 'quota exceeded' in error_message.lower():
            error_message = 'YouTube API quota exceeded. Please try again later or check your API key limits.'
        elif 'not found' in error_message.lower():
            error_message = 'Channel not found. Please check the URL and ensure the channel exists and is public.'
        elif 'invalid' in error_message.lower():
            error_message = 'Invalid channel URL. Please use formats like: @handle, www.youtube.com/@handle, or full channel URL.'
        
        return Response(
            {
                'error': True,
                'message': error_message,
                'help': 'Accepted formats: @handle, www.youtube.com/@handle, https://www.youtube.com/@handle'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        return Response(
            {
                'error': True,
                'message': 'An unexpected error occurred while fetching videos. Please try again.',
                'details': str(e) if request.data.get('debug') else None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
