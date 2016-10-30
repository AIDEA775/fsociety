import json
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from django.utils.html import conditional_escape

from django.http import Http404, HttpResponse

from django.apps import apps

from .models import Comment


def index(request, video_id):
    app, model = settings.VIDEO_MODEL.split('.')
    video_model = apps.get_model(app, model)

    if video_model.objects.filter(pk=video_id).exists():
        return render(request, 'chat_room/index.html', {'id': video_id})
    else:
        raise Http404("Chat Room does not exist")


def api(request, video_id):
    app, model = settings.VIDEO_MODEL.split('.')
    video = get_object_or_404(apps.get_model(app, model), pk=video_id)

    if request.method != 'POST':
        return HttpResponse("Invalid request")

    msg = request.POST.get('msg', None)

    last_seen_id = None

    if Comment.objects.all():
        last_seen_id = request.POST.get('last_seen_id', None)

    if msg and msg.replace(' ', '') is not "":
        Comment.objects.create(author=request.user, from_video=video, msg=msg)

    if last_seen_id:
        last_id_in_db = Comment.objects.latest('pk').pk
        last_seen_id = max(last_seen_id, last_id_in_db - 20)
        query_result = Comment.objects.filter(pk__gt=last_seen_id).order_by('-date_published')
    else:
        query_result = Comment.objects.order_by('-date_published')[:20]

    result = []
    for comment in reversed(query_result):
        result.append(
            {
                'id': comment.id,
                'user_id': comment.author.id,
                'user': conditional_escape(comment.author.get_full_name()),
                'msg': conditional_escape(comment.msg),
                'date': comment.date_published.strftime('%I:%M:%S %p').lstrip('0')
            }
        )

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")
