from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from video_room.models import VideoRoom, VideoRoomUsers
from video.models import Video, WatchedVideo


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    friends = VideoRoomUsers.objects.filter(user__friendship__in=friendship_list)
    most_viewed = Video.objects.order_by('views')[:10]
    context = {'friend_watching': friends,
               'most_viewed': most_viewed}
    return render(request, "video_room/feed.html", context)


@login_required
def join(request, room_id):
    room, _ = VideoRoom.objects.get_or_create(id=room_id)

    _, created = WatchedVideo.objects.update_or_create(user=request.user,
                                                       video=room.video)

    video_list = Video.objects.all().exclude(id=room.video.id)

    context = {'room': room, 'video_list': video_list}
    return render(request, "video_room/player.html", context)


@login_required
def new(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    room = VideoRoom.objects.create(video=video)
    return redirect(reverse('video_room:join', kwargs={'room_id': room.id}))
