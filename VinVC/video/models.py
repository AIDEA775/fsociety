from django.db import models
from django.utils import timezone
from django.conf import settings
from .validators import validate_file_extension


class Document(models.Model):
    title = models.CharField(blank=True, max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    date_upload = models.DateTimeField('date upload', default=timezone.now)
    document_file = models.FileField(upload_to="documents/%Y/%m/%d",
                                     validators=[validate_file_extension])
    description = models.CharField(blank=True, max_length=200, default="")

    def __str__(self):
        return "Title: {}, Description: {}, Author: {}, Date: {}, File: {}"\
            .format(self.title, self.description, self.author,
                    self.date_upload, self.document_file.name)
                    
