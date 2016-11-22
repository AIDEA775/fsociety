from django.db import models
from video.models import Video
from django.utils import timezone
from django.conf import settings


class VideoRoom(models.Model):
    paused = models.BooleanField(default=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    started_playing = models.DateTimeField('started playing', default=timezone.now)
    current_time = models.IntegerField(default=0)

    def __str__(self):
        return "Video: {}, Paused: {}".format(self.video, self.paused)


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
