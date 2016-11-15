from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.conf import settings
from .models import Video, WatchingVideo
import subprocess


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    watched_videos = WatchingVideo.objects.filter(user__friendship__in=
                                                  friendship_list).\
        values('video')
    watching = Video.objects.filter(pk__in=watched_videos)
    most_viewed = Video.objects.order_by('views')[:10]
    context = {'friend_watching': watching,
               'most_viewed': most_viewed}
    return render(request, "video/feed.html", context)


@login_required
def upload(request):
    title = request.POST.get('title')
    video_file = request.FILES.get('video_file')
    description = request.POST.get('description')
    author = request.user

    if all([title, video_file]):
        new_video = Video(title=title,
                          video_file=video_file,
                          description=description,
                          author=author)

        try:
            Video.clean_fields(new_video)
        except ValidationError:
            return render(request, 'video/upload.html',
                          {'error': 'Video not supported'})

        new_video.save()
        thumbnail_id = new_video.id
        new_thumbnail = "{}/videos/{}/{}/{}/".format(settings.MEDIA_URL,
                                                     timezone.now().year,
                                                     timezone.now().month,
                                                     timezone.now().day) + \
                        str(title) + '_' + str(thumbnail_id) + str('.jpg')

        subprocess.call(['ffmpeg', '-y', '-i', '{}'.format(new_video.
                                                           video_file.path),
                         '-vf', 'thumbnail,scale=640:360', '-frames:v', '1',
                         '{}'.format(new_thumbnail)])
        new_video.thumbnail = new_thumbnail
        new_video.save()

    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, "video/upload.html", context)


@login_required
def delete(request):
    try:
        video = Video.objects.get(id=request.GET['id'])
    except(KeyError, Video.DoesNotExist):
        return redirect('user:uploaded', user_id=request.user.id)

    if video.author == request.user:
        video.delete()
        return redirect('user:uploaded', user_id=request.user.id)
    else:
        return HttpResponseForbidden("Don't you have permission to delete")


@login_required
def player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    WatchingVideo.objects.create(user=request.user, video=video)
    context = {'video': video}
    return render(request, "video/player.html", context)
