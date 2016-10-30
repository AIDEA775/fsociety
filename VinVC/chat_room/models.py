from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    from_video = models.ForeignKey(settings.VIDEO_MODEL,
                               on_delete=models.CASCADE)
    msg = models.TextField(max_length=200)
    date_published = models.DateTimeField('date sent', default=timezone.now)
