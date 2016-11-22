from django.db import models
from django.utils import timezone
from video.models import Video


class VideoRoom(models.Model):
    paused = models.BooleanField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    started_playing = models.DateTimeField('started playing', default=timezone.now)
    current_time = models.IntegerField(default=0)

    def __str__(self):
        return "Video: {}, Paused: {}".format(self.video, self.paused)
