"""
URL configuration for youtube_channel_fetcher project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('videos.urls')),
]

