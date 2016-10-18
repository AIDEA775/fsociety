from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Friendship

@login_required
def index(request):
    try:
        user_friendship = request.user.friendship
    except Friendship.DoesNotExist:
        user_friendship = Friendship(user=request.user)
        user_friendship.save()

    friendship_requests_list = user_friendship.getFriendshipRequests()
    context = {'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/index.html', context)

@login_required
def friends(request):
    try:
        user_friendship = request.user.friendship
    except Friendship.DoesNotExist:
        user_friendship = Friendship(user=request.user)
        user_friendship.save()

    friendship_list = user_friendship.friends.all()
    context = {'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)
