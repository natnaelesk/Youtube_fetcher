"""
Serializers for video API responses.
"""

from rest_framework import serializers


class VideoSerializer(serializers.Serializer):
    """Serializer for individual video data."""
    video_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.URLField()
    published_at = serializers.DateTimeField()
    video_url = serializers.URLField()


class ChannelVideosRequestSerializer(serializers.Serializer):
    """Serializer for channel videos request."""
    channel_url = serializers.CharField(required=True, help_text="YouTube channel URL or handle")
    limit = serializers.IntegerField(required=False, default=500, min_value=1, max_value=1000, help_text="Number of videos to fetch")
    offset = serializers.IntegerField(required=False, default=0, min_value=0, help_text="Offset for pagination")


class ChannelVideosResponseSerializer(serializers.Serializer):
    """Serializer for channel videos response."""
    channel_title = serializers.CharField()
    channel_id = serializers.CharField()
    total_videos = serializers.IntegerField()
    videos = VideoSerializer(many=True)
    has_more = serializers.BooleanField(required=False)
    next_offset = serializers.IntegerField(required=False)

