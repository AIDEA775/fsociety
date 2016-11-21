from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from video_room.models import VideoRoom
from chat_room.models import Comment
from video.models import Video, WatchingVideo


@login_required
def player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    WatchingVideo.objects.create(user=request.user, video=video)
    # video_room = VideoRoom.get_or_create(video=video, chat_room=)
    videos = Video.objects.all().exclude(id=video_id)
    context = {'video': video, 'videos': videos}
    # context = {'room': video_room, 'videos': videos}
    return render(request, "video_room/player.html", context)
