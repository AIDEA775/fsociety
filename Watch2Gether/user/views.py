from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Friendship, FriendshipRequest

@login_required
def index(request):
    user_friendship, _ = Friendship.objects.get_or_create(user=request.user)

    friendship_requests_list = user_friendship.getFriendshipRequests()
    context = {'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/index.html', context)

@login_required
def friends(request):
    user_friendship, _ = Friendship.objects.get_or_create(user=request.user)

    friendship_list = user_friendship.friends.all()
    context = {'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)

@login_required
def friendship_accept(request):
    user_friendship, _ = Friendship.objects.get_or_create(user=request.user)

    try:
        friendship_request = user_friendship.getFriendshipRequests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.accept()
    user_friendship.addFriend(friendship_request.sender)
    return HttpResponseRedirect(reverse('user:index'))

@login_required
def friendship_reject(request):
    user_friendship, _ = Friendship.objects.get_or_create(user=request.user)

    try:
        friendship_request = user_friendship.getFriendshipRequests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.reject()
    return HttpResponseRedirect(reverse('user:index'))
