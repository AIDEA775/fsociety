import json
import logging

from django.conf import settings
from django.apps import apps
from django.utils.html import conditional_escape

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Comment

log = logging.getLogger(__name__)


def get_topic_from_path(path):
    app, model = settings.TOPIC_MODEL.split('.')
    topic_model = apps.get_model(app, model)

    pk = path.strip('/').split('/')[-1]
    try:
        topic = topic_model.objects.get(pk=pk)
        return topic
    except ValueError:
        log.debug('message does not contain ws path')
    except topic_model.DoesNotExist:
        log.debug('ws room does not exist pk=%s', pk)


def add_user_to_room(user_message, room_number):
    Group('chat-' + str(room_number), channel_layer=user_message.channel_layer).add(user_message.reply_channel)
    user_message.channel_session['room'] = room_number


@channel_session_user_from_http
def ws_connect(message):
    topic = get_topic_from_path(message['path'])
    if topic is not None:
        add_user_to_room(message, topic.pk)


@channel_session_user
def ws_receive(message):
    app, model = settings.TOPIC_MODEL.split('.')
    topic_model = apps.get_model(app, model)

    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        pk = message.channel_session['room']
        topic = topic_model.objects.get(pk=pk)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except topic_model.DoesNotExist:
        log.debug('received message, buy room does not exist pk=%s', pk)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text")
        return

    if set(data.keys()) != {'msg'}:
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s message=%s', pk, data['msg'])
        msg = data['msg']
        comment = Comment.objects.create(author=message.user, topic=topic, msg=msg)

        Group('chat-' + str(pk), channel_layer=message.channel_layer).send({'text': json.dumps(
            {'user_id': message.user.id,
             'user': conditional_escape(comment.author.get_full_name()),
             'msg': conditional_escape(comment.msg),
             'date': comment.date_published.isoformat()
             }
        )})


@channel_session_user
def ws_disconnect(message):
    app, model = settings.TOPIC_MODEL.split('.')
    topic_model = apps.get_model(app, model)

    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        pk = message.channel_session['room']
        topic_model.objects.get(pk=pk)
        Group('chat-' + str(pk), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, topic_model.DoesNotExist):
        pass