import json
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.http import HttpResponse

from django.apps import apps

from .models import Comment


def index(request, video_id):
    return render(request, 'chat_room/index.html', {'id': video_id})


@csrf_exempt
def api(request, video_id):
    video = get_object_or_404(apps.get_model(*settings.VIDEO_MODEL.split('.')), pk=video_id)

    last_seen_id = None

    if request.method == 'POST':
        msg = request.POST.get('msg', None)

        if Comment.objects.all():
            last_seen_id = request.POST.get('last_seen_id',
                                            Comment.objects.latest('pk').pk)

        if msg and msg.replace(' ', '') is not "":
            Comment.objects.create(author=request.user, from_video=video, msg=msg)

    if last_seen_id:
        query_result = Comment.objects.filter(pk__gt=last_seen_id).order_by('-date_published')
    else:
        query_result = Comment.objects.order_by('-date_published')[:20]

    result = []
    for msg in reversed(query_result):
        result.append(
            {
                'id': msg.id,
                'user': msg.author.username,
                'msg': msg.msg,
                'date': msg.date_published.strftime('%I:%M:%S %p').lstrip('0')
            }
        )

    data = json.dumps(result)

    return HttpResponse(data, content_type="application/json")
