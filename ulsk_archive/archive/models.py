from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)

    def clean(self):
        if not self.video_url and not self.video_file:
            raise ValidationError('Either a video URL or a video file must be provided.')
        if self.video_url and self.video_file:
            raise ValidationError('Only one of video URL or video file can be provided.')

    def __str__(self):
        return self.title