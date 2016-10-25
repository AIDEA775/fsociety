from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def search(request):
    if request.method == 'GET':
        key = request.GET['key']
        users = get_user_model().objects.filter( \
            Q(username__icontains=key) | \
            Q(email__icontains=key) | \
            Q(first_name__icontains=key) | \
            Q(last_name__icontains=key))
        # todo video filter
        videos = None
        context = {'key' : key,
                   'users_results' : users,
                   'videos_results' : videos}
        return render(request, 'search/result.html', context)
