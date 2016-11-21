from django.db import models
from video.models import Video


class VideoRoom(models.Model):
    PAUSED = 0
    PLAYING = 1

    STATUS = (
        (PLAYING, 'Playing'),
        (PAUSED, 'Paused'),
    )

    status = models.IntegerField(choices=STATUS, default=PAUSED)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return "Video: {}, Status: {}".format(self.video, self.status)
