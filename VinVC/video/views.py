from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video, WatchingVideo
from django.core.exceptions import ValidationError


@login_required
def index(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'video/index.html', context)


@login_required
def upload(request):
    """Create a new video."""
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

    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, "video/upload.html", context)


@login_required
def delete(request):
    try:
        video = Video.objects.get(id=request.GET['id'])
        video.delete()
    except(KeyError, Video.DoesNotExist):
        return redirect('video:my_videos')
    return redirect('video:my_videos')


@login_required
def uploaded(request):
    videos = Video.objects.filter(author=request.user)
    context = {'profile': request.user, 'videos': videos}
    return render(request, "video/uploaded.html", context)


@login_required
def friends_videos(request):
    friendship_list = request.user.friendship.get_friends()
    videos = Video.objects.filter(author__friendship__in=friendship_list)
    context = {'videos': videos}
    return render(request, "video/friends_videos.html", context)


@login_required
def add_player(request, video_id):
    user = request.user
    video = Video.objects.all()[video_id]
    WatchingVideo.objects.create(user=user, video=video)


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    watching = WatchingVideo.objects.filter(user__friendship__in=
                                            friendship_list)
    context = {'watching': watching}
    return render(request, "video/feed.html", context)


@login_required
def player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    context = {'video': video}
    return render(request, "video/player.html", context)


@login_required
def most_viewed_videos():
    pass


@login_required
def watched(request):
    pass
