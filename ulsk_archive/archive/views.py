import os
import re
from django.http import StreamingHttpResponse, Http404, HttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render, get_object_or_404
from .models import Video

class RangedFileWrapper:
    def __init__(self, file, start, end, chunk_size=8192):
        self.file = file
        self.file.seek(start)
        self.remaining = end - start + 1
        self.chunk_size = chunk_size

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining <= 0:
            self.close()
            raise StopIteration()
        chunk = self.file.read(min(self.remaining, self.chunk_size))
        if not chunk:
            self.close()
            raise StopIteration()
        self.remaining -= len(chunk)
        return chunk
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def stream_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if not video.video_file:
        raise Http404("Video file not found.")

    path = video.video_file.path
    file_size = os.path.getsize(path)
    
    range_header = request.headers.get('Range')
    if not range_header:
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb'), 8192), content_type='video/mp4')
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes'
        return response

    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    if not range_match:
        return HttpResponse(status=400)

    start_byte = int(range_match.group(1))
    end_byte_str = range_match.group(2)
    if end_byte_str:
        end_byte = int(end_byte_str)
    else:
        end_byte = file_size - 1

    if start_byte >= file_size or end_byte >= file_size or start_byte > end_byte:
        return HttpResponse(status=416)

    content_length = (end_byte - start_byte) + 1

    response = StreamingHttpResponse(RangedFileWrapper(open(path, 'rb'), start_byte, end_byte), status=206, content_type='video/mp4')
    response['Content-Length'] = str(content_length)
    response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{file_size}'
    response['Accept-Ranges'] = 'bytes'
    return response

def index(request):
    return render(request, 'archive/index.html')

def catalog(request):
    videos = Video.objects.all()
    return render(request, 'archive/catalog.html', {'videos': videos})

def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'archive/detail.html', {'video': video})