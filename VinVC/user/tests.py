from django.test import TestCase
from django.contrib.auth import get_user, get_user_model

from .models import Friendship, FriendshipRequest
from login.tests import create_user, login_user


def create_two_users():
    alice = create_user(username="alice", email="alice@example")
    bob = create_user(username="bob", email="bob@example")
    return alice, bob


def friends(user, other):
    user.friendship.send_request(other.friendship)
    other.friendship.get_pending_requests().get().accept()


class UserFriendshipTest(TestCase):
    def setUp(self):
        """
        Create two users, Alice and Bob.
        """
        self.alice, self.bob = create_two_users()

    def test_check_empty_friendship(self):
        self.client.login(username=self.alice.username, password="pass")
        user = get_user(self.client)
        self.assertEqual(user.friendship.get_friends().count(), 0)

    def test_send_friendship_request_and_accept(self):
        self.alice.friendship.send_request(self.bob.friendship)
        requests = self.bob.friendship.get_pending_requests()
        self.assertEqual(requests.count(), 1)
        requests.get().accept()
        self.assertEqual(self.bob.friendship.get_friends().count(), 1)
        self.assertEqual(self.alice.friendship.get_friends().count(), 1)

    def test_send_friendship_request_and_reject(self):
        self.alice.friendship.send_request(self.bob.friendship)
        self.bob.friendship.get_pending_requests().get().reject()
        self.assertEqual(self.bob.friendship.get_friends().count(), 0)
        self.assertEqual(self.alice.friendship.get_friends().count(), 0)
