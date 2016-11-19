from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
from django.db.utils import IntegrityError

from login.tests import LoginUserTest


class UserTest(LoginUserTest):
    """
    Doc here.
    """
    def create_two_users(self):
        alice = self.create_user(username="alice", email="alice@example")
        bob = self.create_user(username="bob", email="bob@example")
        return alice, bob


class UserModelTest(UserTest):
    """
    Doc here. Add more tests using create_two_users()
    """
    def test_create_user_with_duplicate_email(self):
        self.create_user()
        self.assertRaises(IntegrityError, self.create_user, username="otheruser")

    def test_create_user_with_duplicate_username(self):
        self.create_user()
        self.assertRaises(IntegrityError, self.create_user, email="other@example.com")

    def test_count_users_created(self):
        self.assertEqual(get_user_model().objects.count(), 0)
        self.create_user(username="username", email="user@example.com")
        self.assertEqual(get_user_model().objects.count(), 1)
        self.create_user(username="username1", email="user1@example.com")
        self.assertEqual(get_user_model().objects.count(), 2)
