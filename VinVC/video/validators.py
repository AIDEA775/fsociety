from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.web', '.webm', '.mp4', '.egg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
