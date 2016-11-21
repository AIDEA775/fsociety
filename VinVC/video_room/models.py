from django.db import models
from video.models import Video


class VideoRoom(models.Model):
    paused = models.BooleanField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return "Video: {}, Paused: {}".format(self.video, self.paused)
