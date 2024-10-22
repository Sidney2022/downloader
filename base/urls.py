# urls.py
from django.urls import path
from .views import process_link, download_video

urlpatterns = [
    path('', process_link, name='process_link'),  # Displays the form and video details
    path('download/', download_video, name='download_video'),  # Handles the download
]
