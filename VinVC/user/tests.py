from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Friendship, FriendshipRequest


class UserFriendshipTest(TestCase):
    def setUp(self):
        """
        Create two users, alice and bob.
        """
        # Alice id = 1
        get_user_model().objects.create_user("alice", "alice@example", "pass", \
            first_name="alice name", last_name="alice last")
        # Bob id = 2
        get_user_model().objects.create_user("bob", "bob@example", "pass", \
            first_name="bob name", last_name="bob last")

    def test_check_empty_friendship(self):
        self.client.login(username="alice", password="pass")
        response = self.client.get(reverse('user:friends'))
        self.assertEqual(len(response.context['friendship_list']), 0)

    def test_check_one_user_list(self):
        self.client.login(username="alice", password="pass")
        response = self.client.get(reverse('user:list'))
        self.assertEqual(len(response.context['user_status']), 1)

    def test_send_friendship_request_and_accept(self):
        # Login with Alice
        self.client.login(username="alice", password="pass")
        # Send request to Bob
        response = self.client.get(reverse('user:request_send'), {'id' : '2'})
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # Login with Bob
        self.client.login(username="bob", password="pass")
        # View Alice request
        response = self.client.get(reverse('user:index'))
        request_list = response.context['friendship_requests_list']
        self.assertEqual(len(request_list), 1)
        sender_id = request_list[0].sender.id
        self.assertEqual(sender_id, 1)
        # Accept request
        response = self.client.get(reverse('user:request_accept'), {'id' : '1' })
        # Check new friend
        response = self.client.get(reverse('user:friends'))
        self.assertEqual(len(response.context['friendship_list']), 1)
        self.client.logout()

        # Login with Alice and check new friend
        self.client.login(username="alice", password="pass")
        response = self.client.get(reverse('user:friends'))
        self.assertEqual(len(response.context['friendship_list']), 1)
