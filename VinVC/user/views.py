import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils.html import conditional_escape

from .models import FriendshipRequest


@login_required
def requests(request):
    friendship_requests_list = request.user.friendship.get_pending_requests()
    context = {'profile': request.user,
               'friendship_requests_list': friendship_requests_list}
    return render(request, 'user/requests.html', context)


@login_required
def profile(request, user_id):
    my_friendship = request.user.friendship
    profile = get_object_or_404(get_user_model(), pk=user_id)
    status = 'same_user'
    request_id = None
    if profile != request.user:
        status = my_friendship.get_friendship_status(profile)
        if status == 'need_response':
            request_id = my_friendship.get_pending_requests(
                from_user=profile.friendship)[0].id
    context = {'profile': profile, 'status': status, 'request_id': request_id}
    return render(request, 'user/profile.html', context)


@login_required
def friends(request):
    friendship_list = request.user.friendship.friends.all()
    context = {'profile': request.user, 'friendship_list': friendship_list}
    return render(request, 'user/friends.html', context)


@login_required
def request_accept(request):
    try:
        user_friendship = request.user.friendship
        friendship_request = \
            user_friendship.get_pending_requests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return redirect('user:profile')

    friendship_request.accept()
    return redirect('user:profile')


@login_required
def request_reject(request):
    try:
        user_friendship = request.user.friendship
        friendship_request = \
            user_friendship.get_pending_requests().get(id=request.GET['id'])
    except (KeyError, FriendshipRequest.DoesNotExist):
        return redirect('user:profile')

    friendship_request.reject()
    return redirect('user:profile')


@login_required
def list(request):
    my_friendship = request.user.friendship
    users_list = get_user_model().objects.exclude(pk=request.user.pk)

    user_status = []
    for user in users_list:
        user_status.append((user, my_friendship.get_friendship_status(user)))

    context = {'user_status': user_status}
    return render(request, 'user/list.html', context)


@login_required
def request_send(request):
    try:
        user = get_user_model().objects.get(id=request.GET['id'])
        request.user.friendship.send_request(user.friendship)
    except (KeyError, FriendshipRequest.DoesNotExist):
        return redirect('user:list')
    return redirect('user:list')


@login_required
def requests_api(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request")

    valid_methods = {"accept", "reject", "send", "get"}
    api_method = request.POST.get('method', None)

    if api_method not in valid_methods:
        return HttpResponseBadRequest("Invalid request")

    user_friendship = request.user.friendship

    if api_method == "get":
        last_request_seen = request.POST.get('last_request_seen', None)

        if not last_request_seen:
            last_request_seen = -1

        query_result = user_friendship.get_pending_requests()\
            .filter(pk__gt=last_request_seen).order_by('-sent_date')

        result = []
        for friendship_request in reversed(query_result):
            result.append(
                {
                    'id': friendship_request.pk,
                    'user_id': friendship_request.sender.user.id,
                    'user': conditional_escape(friendship_request.sender.user.
                                               get_full_name()),
                }
            )

        data = json.dumps(result)

    elif api_method == "accept" or api_method == "reject":
        try:
            friendship_request = \
                user_friendship.get_pending_requests().get(id=request.
                                                           POST['id'])
        except (KeyError, FriendshipRequest.DoesNotExist):
            raise Http404("Friendship Request does not exist")

        if api_method == "accept":
            friendship_request.accept()
        else:
            friendship_request.reject()

        data = json.dumps({'status': 'OK'})

    else:
        try:
            to_friendship = get_user_model().objects.get(id=request.
                                                         POST['id']).friendship
            user_friendship.send_request(to_friendship)
        except KeyError:
            return HttpResponseBadRequest('Invalid ID')

        data = json.dumps({'status': 'OK'})

    return HttpResponse(data, content_type="application/json")
