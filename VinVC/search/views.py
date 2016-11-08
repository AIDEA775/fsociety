from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from video.models import Video


@login_required
def search(request):
    if request.method == 'GET':
        key = request.GET['key']
        users = None
        videos = None
        if key != '':
            users = get_user_model().objects.filter(
                Q(username__icontains=key) |
                Q(email__icontains=key) |
                Q(first_name__icontains=key) |
                Q(last_name__icontains=key))
            videos = Video.objects.filter(
                Q(title__icontains=key) |
                Q(description__icontains=key))
        context = {'key': key,
                   'user_list': users,
                   'video_list': videos}
        return render(request, 'search/result.html', context)
