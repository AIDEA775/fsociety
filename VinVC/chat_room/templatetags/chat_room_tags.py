from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from ..models import Comment


register = template.Library()


@register.simple_tag
def chat_room_headers():
    style_url = static('chat_room/css/style.css')
    ws_url = static('chat_room/js/reconnecting-websocket.min.js')

    result = "<link rel='stylesheet' href='{}' />".format(style_url)
    result += "<script type='text/javascript' src='{}'></script>".format(ws_url)

    return format_html(result)


@register.inclusion_tag('chat_room/chat_room.html', takes_context=True)
def show_chat_room(context, chat_room_id):
    # We want to show the last 20 messages, ordered most-recent-last
    messages = reversed(Comment.objects.filter(topic=chat_room_id).order_by('-date_published')[:20])

    return {'user_id': context['request'].user.id,
            'chat_room_id': chat_room_id,
            'messages': messages}
