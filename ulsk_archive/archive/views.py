from django.shortcuts import render, get_object_or_404
from .models import Video

def index(request):
    return render(request, 'archive/index.html')

def catalog(request):
    videos = Video.objects.all()
    return render(request, 'archive/catalog.html', {'videos': videos})

def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'archive/detail.html', {'video': video})