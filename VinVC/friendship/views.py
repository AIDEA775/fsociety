from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils.html import conditional_escape

import json

from .models import FriendshipRequest

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
