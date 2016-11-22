from django.db import models
from video.models import Video
from django.utils import timezone
from django.conf import settings


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


class VideoRoomUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user')
    room = models.ForeignKey(VideoRoom, on_delete=models.CASCADE,
                              related_name='room')
    date = models.DateTimeField('date view', default=timezone.now)

    def __str__(self):
        return "User: {}, Room: <<{}>>, Date: {}".format(self.user,
                                                          self.room,
                                                          self.date)
