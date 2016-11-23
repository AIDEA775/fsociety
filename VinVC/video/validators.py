from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
import magic
import os


def validate_file_extension(upload):
    tmp_path = 'tmp/ %s ' % upload.name[2:]
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    if file_type not in settings.VIDEO_TYPES:
        raise ValidationError('File type not supported.')
