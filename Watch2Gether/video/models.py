from django.db import models
from .validators import validate_file_extension


class Document(models.Model):
    name = models.CharField(max_length=100)
    # author = models.ForeignKey(User, to_field='id', related_name="id_user2")
    # date_upload = models.DateField()
    docfile = models.FileField(upload_to="documents/%Y/%m/%d",
                               validators=[validate_file_extension])
    description = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return "Video: {}".format(self.docfile.name)
