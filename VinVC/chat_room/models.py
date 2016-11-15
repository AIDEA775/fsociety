from django.db import models
from django.utils import timezone
from django.conf import settings


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    topic = models.ForeignKey(settings.TOPIC_MODEL,
                              on_delete=models.CASCADE)
    msg = models.TextField(max_length=200)
    date_published = models.DateTimeField('date sent', default=timezone.now)
