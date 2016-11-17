from django.db import models
from video.models import Video
from chat_room.models import Comment


class VideoRoom(models.Model):
    videos = models.ManyToManyField(Video,
                                    through='VRVideos',
                                    through_fields=('room', 'video'),
                                    symmetrical=True,
                                    related_name='video_room')

    chat_room = models.ForeignKey(Comment,
                                  on_delete=models.CASCADE)


class VRVideos(models.Model):
    room = models.ForeignKey(VideoRoom,
                             on_delete=models.CASCADE,
                             related_name='room')
    video = models.ForeignKey(Video,
                              on_delete=models.CASCADE,
                              related_name='video')
