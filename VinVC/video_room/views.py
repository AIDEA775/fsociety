from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from video_room.models import VideoRoom
from video.models import Video, WatchingVideo


@login_required
def player(request, video_id, chat_room=None):
    video = get_object_or_404(Video, id=video_id)
    WatchingVideo.objects.create(user=request.user, video=video)
    video_room, created = VideoRoom.objects.get_or_create(video=video)
    videos = Video.objects.all().exclude(id=video_id)
    if chat_room is None:
        chat_room = video_room.pk
    context = {'video': video_room, 'chat': chat_room, 'videos': videos}
    return render(request, "video_room/player.html", context)
