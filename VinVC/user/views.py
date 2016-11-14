import json
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils.html import conditional_escape

from .models import FriendshipRequest
from video.models import Video, WatchingVideo
from .forms import EditUserForm

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

    context = {'profile': profile,
               'status': status,
               'request_id': request_id}

    return render(request, 'user/profile.html', context)


@login_required
def requests(request):
    full = request.GET.get('full', "true")
    if full == 'false':
        friendship_requests_list = request.user.friendship.get_pending_requests()
        context = {'profile': request.user,
                   'friendship_requests_list': friendship_requests_list}
        return render(request, 'user/requests.html', context)
    else:
        return redirect('{}#requests'.format(reverse('user:profile',
                        kwargs={'user_id': request.user.id})))


@login_required
def friends(request, user_id):
    full = request.GET.get('full', "true")
    user = get_object_or_404(get_user_model(), id=user_id)
    if full == 'false':
        friendship_list = user.friendship.friends.all()
        context = {'profile': request.user, 'friendship_list': friendship_list}
        return render(request, 'user/friends.html', context)
    else:
        return redirect('{}#friends'.format(reverse('user:profile',
                        kwargs={'user_id': user.id})))


@login_required
def uploaded(request, user_id):
    full = request.GET.get('full', "true")
    user = get_object_or_404(get_user_model(), id=user_id)
    if full == 'false':
        videos = Video.objects.filter(author=user)
        context = {'profile': request.user, 'video_list': videos}
        return render(request, "user/uploaded.html", context)
    else:
        return redirect('{}#uploaded'.format(reverse('user:profile',
                        kwargs={'user_id': user.id})))


@login_required
def watched(request, user_id):
    full = request.GET.get('full', "true")
    user = get_object_or_404(get_user_model(), id=user_id)
    if full == 'false':
        watched_videos = WatchingVideo.objects.filter(user=user).values('video')
        videos = Video.objects.filter(pk__in=watched_videos)
        context = {'profile': user, 'video_list': videos}
        return render(request, "user/watched.html", context)
    else:
        return redirect('{}#watched'.format(reverse('user:profile',
                        kwargs={'user_id': user.id})))


@login_required
def edit(request):
    if request.method == 'POST':
        pass
    else:
        form = EditUserForm()
    return render(request, 'user/edit.html', {'form': form})


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
