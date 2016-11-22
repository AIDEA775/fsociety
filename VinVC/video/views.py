from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from os.path import dirname, relpath, join
import subprocess
import os
from .models import Video, WatchingVideo
from .forms import VideoUploadForm


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    friends = WatchingVideo.objects.filter(user__friendship__in=friendship_list)
    most_viewed = Video.objects.order_by('views')[:10]
    context = {'friend_watching': friends,
               'most_viewed': most_viewed}
    return render(request, "video/feed.html", context)


def get_new_thumbnail_path(new_video):
    return join(relpath(dirname(new_video.video_file.path), 'media'),
                str(new_video.id) + '.jpg')


@login_required
def upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.author = request.user
            new_video.save()

            new_video.thumbnail = get_new_thumbnail_path(new_video)
            new_video.save()
            subprocess.call('ffmpeg -v error -y -i {} -vf '
                            'thumbnail,scale=640:360 -vframes 1 media/{}'
                            .format(new_video.video_file.path,
                                    new_video.thumbnail),
                            shell=True)
            return redirect('video:feed')
    else:
        form = VideoUploadForm()
    return render(request, 'video/upload.html', {'form': form})


@login_required
def delete(request):
    try:
        video = Video.objects.get(id=request.GET['id'])
    except(KeyError, Video.DoesNotExist):
        return redirect('user:uploaded', user_id=request.user.id)

    if video.author == request.user:
        os.remove(video.thumbnail.path)
        os.remove(video.video_file.path)
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
