"""
URL routing for videos app.
"""

from django.urls import path
from videos import views

urlpatterns = [
    path('channel/videos/', views.fetch_channel_videos, name='fetch_channel_videos'),
]

