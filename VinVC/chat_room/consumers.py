import json
import logging

from django.conf import settings
from django.apps import apps
from django.utils.html import conditional_escape

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import Comment

log = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat_room/{pk}/, and finds the related Topic if the message path is
    # applicable, and if the related Topic exists. Otherwise, bails (meaning
    # this is a some other sort of websocket)

    app, model = settings.TOPIC_MODEL.split('.')
    topic_model = apps.get_model(app, model)

    try:
        pk = message['path'].strip('/').split('/')[-1]
        topic_model.objects.get(pk=pk)
    except ValueError:
        log.debug('message does not contain ws path')
        return
    except topic_model.DoesNotExist:
        log.debug('ws room does not exist pk=%s', pk)
        return

    log.debug('chat connect room=%s client=%s:%s',
              pk, message['client'][0], message['client'][1])

    Group('chat-' + pk, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = pk


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

        Group('chat-' + pk, channel_layer=message.channel_layer).send({'text': json.dumps(
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
        Group('chat-' + pk, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, topic_model.DoesNotExist):
        pass
