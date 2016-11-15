from django.db import models
from django.utils import timezone
from django.conf import settings
from .validators import validate_file_extension


class Video(models.Model):
    title = models.CharField(blank=True, max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author')
    date_upload = models.DateTimeField('date upload', default=timezone.now)
    video_file = models.FileField(upload_to="videos/%Y/%m/%d",
                                  validators=[validate_file_extension])
    thumbnail = models.ImageField(upload_to="videos/%Y/%m/%d", blank=True)
    description = models.CharField(blank=True, max_length=200, default="")
    views = models.IntegerField(default=0)
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='WatchingVideo',
                                      through_fields=('video', 'user'),
                                      symmetrical=False)

    def __str__(self):
        return "Title: {}, Description: {}, Author: {}, Date: {}, File: {}, " \
               "Views: {}, Watchers: {}, Thumbnail: {}".format(self.title, self.description,
                                                               self.author, self.date_upload,
                                                               self.video_file.name,
                                                               self.views, self.watchers.all(),
                                                               self.thumbnail)


class WatchingVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='video')
    date = models.DateTimeField('date view', default=timezone.now)
