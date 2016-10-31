from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html


register = template.Library()


@register.simple_tag
def chat_room_headers():
    style_url = static('chat_room/css/style.css')

    result = "<link rel='stylesheet' href='{}' />".format(style_url)

    return format_html(result)


@register.inclusion_tag('chat_room/chat_room.html', takes_context=True)
def show_chat_room(context, chat_room_id):
    return {'user_id': context['request'].user.id,
            'chat_room_id': chat_room_id}
