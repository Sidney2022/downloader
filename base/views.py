# views.py
from django.shortcuts import render, redirect
from pytubefix import YouTube
from django.http import HttpResponse
import os
import yt_dlp

# Handle the form submission and display the video thumbnail
# def process_link(request):
#     if request.method == 'POST':
#         youtube_url = request.POST.get('youtube_url')
#         try:
#             # Initialize YouTube object to get video details
#             yt = YouTube(youtube_url)
#             video = {
#                 'title': yt.title,
#                 'thumbnail_url': yt.thumbnail_url,
#                 'url': youtube_url  # Pass the URL again for the download step
#             }
#             return render(request, 'index.html', {'video': video})
#         except Exception as e:
#             # Handle the case where the URL is invalid or other errors occur
#             return render(request, 'index.html', {'error': 'Invalid YouTube URL or error fetching video.'})
#     # If not a POST request, render the form page
#     return render(request, 'index.html')


def process_link(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        print(f"Received YouTube URL: {youtube_url}")
        try:
            yt = YouTube(youtube_url)
            video = {
                'title': yt.title,
                'thumbnail_url': yt.thumbnail_url,
                'url': youtube_url,
            }
            return render(request, 'index.html', {'video': video})
        except Exception as e:
            print(e)
            return render(request, 'index.html', {'error': 'Invalid YouTube URL or error fetching video.'})

    return render(request, 'index.html')

# Handle the download after confirmation

# views.py

# def download_video(request):
#     if request.method == 'POST':
#         youtube_url = request.POST.get('youtube_url')
#         try:
#             # Set download options
#             ydl_opts = {
#                 'format': 'best',  # Choose the best available quality
#                 'outtmpl': 'downloads/%(title)s.%(ext)s'  # Specify output path
#             }

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([youtube_url])

#             return HttpResponse(f"Download successful!")
#         except Exception as e:
#             return HttpResponse(f"Download failed: {str(e)}")

#     return redirect('process_link')




from django.http import HttpResponse
import os

def download_video(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        media_type = request.POST.get('media_type')  # 'video' or 'audio'

        if not youtube_url or media_type not in ['video', 'audio']:
            return HttpResponse("Invalid request", status=400)

        try:
            vid = YouTube(youtube_url)
            entry = vid.title
            
            if media_type == 'video':
                video_download = vid.streams.get_highest_resolution()
                filename = f"{entry}.mp4"
                print(f"Downloading Video: {filename}")
                video_download.download(filename=filename)
            else:  # media_type == 'audio'
                audio_download = vid.streams.get_audio_only()
                filename = f"{entry}.mp3"
                print(f"Downloading Audio: {filename}")
                audio_download.download(filename=filename)

            # Provide the response with the file
            file_path = os.path.join(os.getcwd(), filename)
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='audio/mp3' if media_type == 'audio' else 'video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
            # Optionally, you can remove the file after serving it
            os.remove(file_path)

            return response

        except Exception as e:
            return HttpResponse(f"Download failed: {str(e)}", status=500)

    return HttpResponse("Invalid request method", status=405)
