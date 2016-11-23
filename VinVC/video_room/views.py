import random
from hashlib import sha1

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db import transaction

from .models import VideoRoom, VideoRoomUsers
from video.models import Video, WatchedUsers


@login_required
def feed(request):
    friendship_list = request.user.friendship.get_friends()
    friends = VideoRoomUsers.objects.filter(user__friendship__in=friendship_list)
    most_viewed = Video.objects.order_by('-views')[:10]
    context = {'friend_watching': friends,
               'most_viewed': most_viewed}
    return render(request, "video_room/feed.html", context)


@login_required
def join(request, label):
    room = get_object_or_404(VideoRoom, label=label)

    _, created = WatchedUsers.objects.update_or_create(user=request.user,
                                                       video=room.video)

    if created:
        room.video.update_views()

    video_list = Video.objects.all().exclude(id=room.video.id)

    context = {'room': room, 'video_list': video_list}
    return render(request, "video_room/player.html", context)


def random_label():
    while True:
        with transaction.atomic():
            label = sha1(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
            if not VideoRoom.objects.filter(label=label).exists():
                break
    return label

@login_required
def new(request, video_id):
    """
    Randomly create a new room, and redirect to it.
    """
    video = get_object_or_404(Video, id=video_id)
    new_room = VideoRoom.objects.create(video=video, label=random_label())
    return redirect(reverse('video_room:join', kwargs={'label': new_room.label}))
