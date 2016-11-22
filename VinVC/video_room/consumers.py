import json
import logging

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils import timezone

from .models import VideoRoom

log = logging.getLogger(__name__)


def get_room_from_path(path):
    pk = path.strip('/').split('/')[-1]
    try:
        room = VideoRoom.objects.get(pk=pk)
        return room
    except ValueError:
        log.debug('message does not contain ws path')
    except VideoRoom.DoesNotExist:
        log.debug('ws room does not exist pk=%s', pk)


def add_user_to_room(user_message, room_number):
    Group('video-room-' + str(room_number), channel_layer=user_message.channel_layer).add(user_message.reply_channel)
    user_message.channel_session['video-room'] = room_number


def send_room_status_to_user(user_message, room):
    if not room.paused:
        current_time = (timezone.now() - room.started_playing).total_seconds()
    else:
        current_time = room.current_time

    user_message.reply_channel.send({'text': json.dumps(
            {'paused': room.paused,
             'current_time': current_time,
             }
        )}
    )

@channel_session_user_from_http
def ws_connect(message):
    room = get_room_from_path(message['path'])
    if room is not None:
        add_user_to_room(message, room.pk)
        send_room_status_to_user(message, room)


@channel_session_user
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        pk = message.channel_session['video-room']
        room = VideoRoom.objects.get(pk=pk)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except VideoRoom.DoesNotExist:
        log.debug('received message, buy room does not exist pk=%s', pk)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text")
        return

    if set(data.keys()) != {'paused', 'current_time'}:
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s paused=%s, current_time=%s', pk, data['paused'], data['current_time'])

        paused = data['paused']
        room.current_time = int(data['current_time'])

        if paused:
            room.paused = True
            room.started_playing = timezone.now() - timezone.timedelta(seconds=room.current_time)
        else:
            room.paused = False

        room.save()

        Group('video-room-' + str(pk), channel_layer=message.channel_layer).send({'text': json.dumps(
            {'paused': room.paused,
             'current_time': room.current_time,
             }
        )})


@channel_session_user
def ws_disconnect(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        pk = message.channel_session['video-room']
        VideoRoom.objects.get(pk=pk)
        Group('video-room-' + str(pk), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, VideoRoom.DoesNotExist):
        pass
