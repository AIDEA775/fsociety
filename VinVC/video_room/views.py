from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from video_room.models import VideoRoom, VideoRoomUsers
from video.models import Video


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    friends = VideoRoomUsers.objects.filter(user__friendship__in=friendship_list)
    most_viewed = Video.objects.order_by('views')[:10]
    context = {'friend_watching': friends,
               'most_viewed': most_viewed}
    return render(request, "video_room/feed.html", context)


@login_required
def player(request, video_id, chat_id=''):
    video = get_object_or_404(Video, id=video_id)

    # TODO Check if with chat_room = None this return new VideoRoom
    room, new = VideoRoom.objects.get_or_create(room=room_id)

    VideoRoomUsers.objects.create(user=request.user, room=room)
    videos = Video.objects.all().exclude(id=video_id)

    # TODO Here? check context
    context = {'video': video_room, 'chat': room, 'videos': videos}
    return render(request, "video_room/player.html", context)
