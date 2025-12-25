from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video_url', 'video_file', 'cover_image')
    search_fields = ('title',)
    fields = ('title', 'description', 'video_url', 'video_file', 'cover_image')