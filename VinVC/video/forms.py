from django import forms

from .models import Video
from .validators import validate_file_extension


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']
