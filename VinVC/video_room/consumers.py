import json
import logging

from math import ceil

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils import timezone

from .models import VideoRoom, VideoRoomUsers
from video.models import Video

log = logging.getLogger(__name__)


def get_room_from_number(room_number):
    try:
        room = VideoRoom.objects.get(pk=room_number)
        return room
    except VideoRoom.DoesNotExist:
        log.debug('received message, buy room does not exist pk=%s', room_number)
        return


def get_room_from_path(path):
    pk = path.strip('/').split('/')[-1]
    try:
        return get_room_from_number(pk)
    except ValueError:
        log.debug('message does not contain ws path')


def add_user_to_room(user_message, room):
    VideoRoomUsers.objects.create(user=user_message.user, room=room)
    Group('video-room-' + str(room.pk), channel_layer=user_message.channel_layer).add(user_message.reply_channel)
    user_message.channel_session['video-room'] = room.pk


def send_room_status_to_user(user_message, room):
    if not room.paused:
        current_time = ceil((timezone.now() - room.started_playing).total_seconds())
    else:
        current_time = room.current_time

    user_message.reply_channel.send({'text': json.dumps(
            {
                'method': 'update',
                'paused': room.paused,
                'current_time': current_time,
            }
        )}
    )


@channel_session_user_from_http
def ws_connect(message):
    room = get_room_from_path(message['path'])
    if room is not None:
        add_user_to_room(message, room)
        send_room_status_to_user(message, room)


def get_data_from_message(message):
    try:
        data = json.loads(message['text'])
        return data
    except ValueError:
        log.debug("ws message isn't json text")
        return


def is_data_malformed(data):
    try:
        if data['method'] == 'update':
            return set(data.keys()) != {'method', 'paused', 'current_time'}
        elif data['method'] == 'change':
            return set(data.keys()) != {'method', 'id'}
    except KeyError:
        return False


@channel_session_user
def ws_receive(message):
    room = get_room_from_number(message.channel_session['video-room'])
    if not room:
        return

    data = get_data_from_message(message)
    if not data:
        return

    if is_data_malformed(data):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data['method'] == 'change':
        try:
            new_video = Video.objects.get(pk=int(data['id']))
            room.video = new_video
            room.paused = False
            room.current_time = 0
            room.started_playing = timezone.now()
            room.save()
        except Video.DoesNotExist:
            return

        Group('video-room-' + str(room.pk), channel_layer=message.channel_layer).send({'text': json.dumps(
            {
                'method': 'change',
            }
        )})

    elif data['method'] == 'force':
        send_room_status_to_user(message, room)

    elif data['method'] == 'update':
        paused = data['paused']
        if paused == room.paused:
            return

        room.paused = paused
        room.current_time = float(data['current_time'])
        room.started_playing = timezone.now() - timezone.timedelta(seconds=room.current_time)
        room.save()

        Group('video-room-' + str(room.pk), channel_layer=message.channel_layer).send({'text': json.dumps(
            {
                'method': 'update',
                'paused': room.paused,
                'current_time': room.current_time,
            }
        )})


@channel_session_user
def ws_disconnect(message):
    try:
        pk = message.channel_session['video-room']
        VideoRoom.objects.get(pk=pk)
        VideoRoomUsers.objects.filter(user=message.user).delete()
        Group('video-room-' + str(pk), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, VideoRoom.DoesNotExist):
        pass
