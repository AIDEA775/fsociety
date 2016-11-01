from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
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
        new_doc = Video(title=title,
                        video_file=video_file,
                        description=description,
                        author=author)

        try:
            Video.clean_fields(new_doc)
        except ValidationError:
            return render(request, 'video/upload.html', {'error': 'Video not supported'})

        new_doc.save()

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
def my_videos(request):
    videos = Video.objects.filter(author=request.user)
    context = {'videos': videos}
    return render(request, "video/my_videos.html", context)


@login_required
def friends_videos(request):
    friendship_list = request.user.friendship.get_friends()
    videos = Video.objects.filter(author__friendship__in=friendship_list)
    context = {'videos': videos}
    return render(request, "video/friends_videos.html", context)
    
@login_required
def top(request):
    print (Video.objects.all())
    videos = Video.objects.order_by('views')[10:]
    print (videos)
    context = {'videos':videos}
    return render(request, "video/top.html", context)
