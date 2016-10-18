from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models

@login_required
def index(request):
    if request.user.friendship is None:
        models.Friendship(user=request.user).save()

    friendship_requests_list = request.user.friendship.getFriendshipRequests()
    context = {'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/index.html', context)

@login_required
def friends(request):
    if request.user.friendship is None:
        models.Friendship(user=request.user).save()

    friendship_list = request.user.friendship.friends.all()
    context = {'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)
