from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Friendship, FriendshipRequest

@login_required
def index(request):
    friendship_requests_list = request.user.friendship.getFriendshipRequests()
    context = {'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/index.html', context)

@login_required
def friends(request):
    friendship_list = request.user.friendship.friends.all()
    context = {'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)

@login_required
def friendship_accept(request):
    try:
        friendship_request = request.user.friendship.getFriendshipRequests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.accept()
    return HttpResponseRedirect(reverse('user:index'))

@login_required
def friendship_reject(request):
    try:
        friendship_request = request.user.friendship.getFriendshipRequests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.reject()
    return HttpResponseRedirect(reverse('user:index'))
