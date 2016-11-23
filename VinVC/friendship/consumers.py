import json
import logging

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils.html import conditional_escape
from django.contrib.auth import get_user_model

from .models import FriendshipRequest

log = logging.getLogger(__name__)


def add_user_to_group(message):
    Group('user-' + str(message.user.pk), channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['user'] = message.user.pk


def get_friendship_request_list(user):
    query_result = user.friendship.get_pending_requests().order_by('-sent_date')[:20]

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
    return data


def send_friendship_requests(message):
    requests = get_friendship_request_list(message.user)
    message.reply_channel.send({'text': requests})


@channel_session_user_from_http
def ws_connect(message):
    add_user_to_group(message)
    send_friendship_requests(message)


def get_data_from_message(message):
    try:
        data = json.loads(message['text'])
        return data
    except ValueError:
        log.debug("ws message isn't json text")
        return


def is_valid_method(method):
    valid_methods = {'accept', 'reject', 'send'}
    return method in valid_methods


def is_data_malformed(data):
    try:
        if not is_valid_method(data['method']):
            return True

        return False
    except KeyError:
        return True


def accept_friendship_request(user, request_id):
    try:
        friendship_request = \
            user.friendship.get_pending_requests().get(id=request_id)
        friendship_request.accept()
    except (KeyError, FriendshipRequest.DoesNotExist):
        return


def reject_friendship_request(user, request_id):
    try:
        friendship_request = \
            user.friendship.get_pending_requests().get(id=request_id)
        friendship_request.reject()
    except (KeyError, FriendshipRequest.DoesNotExist):
        return


def send_friendship_request(message, receiver_id):
    try:
        receiver_friendship = get_user_model().objects.get(id=receiver_id).friendship
        request_id = message.user.friendship.send_request(receiver_friendship)

        if request_id:
            Group('user-' + str(receiver_id), channel_layer=message.channel_layer).send({'text': json.dumps(
                [{
                    'id': request_id,
                    'user_id': message.user.id,
                    'user': conditional_escape(message.user.get_full_name()),
                }]
            )})
    except (KeyError, FriendshipRequest.DoesNotExist):
        return


@channel_session_user
def ws_receive(message):
    user = message.user
    data = get_data_from_message(message)
    if not data:
        return

    if is_data_malformed(data):
        log.debug("ws message unexpected format data=%s", data)
        return

    method = data['method']
    if method == 'accept':
        accept_friendship_request(user, data['id'])
    elif method == 'reject':
        reject_friendship_request(user, data['id'])
    elif method == 'send':
        send_friendship_request(message, data['id'])


@channel_session_user
def ws_disconnect(message):
    Group('user-' + str(message.user.pk), channel_layer=message.channel_layer).discard(message.reply_channel)
