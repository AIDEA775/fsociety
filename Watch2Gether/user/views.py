from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import FriendshipRequest


@login_required
def home(request):
    friendship_requests_list = request.user.friendship.get_pending_requests()
    context = {'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/index.html', context)


@login_required
def friends(request):
    friendship_list = request.user.friendship.friends.all()
    context = {'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)


@login_required
def request_accept(request):
    try:
        user_friendship = request.user.friendship
        friendship_request = \
            user_friendship.get_pending_requests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.accept()
    return HttpResponseRedirect(reverse('user:index'))


@login_required
def request_reject(request):
    try:
        user_friendship = request.user.friendship
        friendship_request = \
            user_friendship.get_pending_requests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:index'))

    friendship_request.reject()
    return HttpResponseRedirect(reverse('user:index'))


@login_required
def list(request):
    my_friendship = request.user.friendship
    users_list = get_user_model().objects.exclude(pk=request.user.pk)

    user_status = []
    for user in users_list:
        if user.friendship in my_friendship.get_friends():
            user_status.append((user, 'friends'))
        elif user.friendship.get_pending_requests(from_user=my_friendship):
            user_status.append((user, 'already_sent_request'))
        else:
            user_status.append((user, 'allow_send_request'))

    context = {'user_status': user_status}
    return render(request, 'user/list.html', context)


@login_required
def request_send(request):
    try:
        user = get_user_model().objects.get(id=request.GET['id'])
        request.user.friendship.send_request(user.friendship)
    except (KeyError, FriendshipRequest.DoesNotExist):
        return HttpResponseRedirect(reverse('user:list'))
    return HttpResponseRedirect(reverse('user:list'))
