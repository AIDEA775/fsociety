from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Video
import os


@login_required
def list(request):
    """Create a new video."""
    title = request.POST.get('title')
    video_file = request.FILES.get('video_file')
    description = request.POST.get('description')
    author = request.user

    if all([title, video_file]):
        new_doc = Video(title=title,
                        video_file=video_file,
                        description=description,
                        author=author)
        new_doc.save()

    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, "video/list.html", context)


@login_required
def delete(self, *args, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, self.video.name))
    super(Video, self).delete(*args, **kwargs)
