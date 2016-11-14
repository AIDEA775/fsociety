from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
    data ={'first_name': request.user.first_name,
           'last_name' : request.user.last_name,
           'username'  : request.user.username,
           'email'     : request.user.email,
           'password'  : ''
           }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditUserForm(request.POST, initial = data)
        # check whether it's valid:
        if form.is_valid() and form.has_changed():
            first_name = form.cleaned_data('first_name')
            print(first_name)
            last_name = form.cleaned_data('last_name')
            username = form.cleaned_data('username')
            email = form.cleaned_data('email')
            password = form.cleaned_data('password')
            if first_name != request.user.first_name:
                request.user.first_name = first_name
            if last_name != request.user.last_name:
                request.user.last_name = last_name
            if username != request.user.username:
                request.user.username = username
            if email != request.user.email:
                request.user.email = email
            if password:
                request.user.set_password(password)
            request.user.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUserForm(initial=data)
    return render(request, 'user/edit.html', {'form': form})
