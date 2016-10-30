from django.test import TestCase
from django.test import Client
from django.db.utils import IntegrityError
from django.contrib.auth import get_user, get_user_model


def create_user(username="username", email="user@example.com", password="pass",
                first_name="first", last_name="last"):
    return get_user_model().objects.create_user(username, email, password,
        first_name=first_name, last_name=last_name)


def login_user(username="username", password="pass"):
    c = Client()
    c.login(username=username, password=password)
    return c


class LoginUser(TestCase):
    def test_login_user(self):
        """
        Create new user and check if is authenticated.
        """
        create_user()
        self.client = login_user()
        user = get_user(self.client)
        assert user.is_authenticated()

    def test_bad_login_user(self):
        create_user()
        self.client = login_user(password="badpass")
        user = get_user(self.client)
        assert not user.is_authenticated()

    def test_create_user_with_duplicate_email(self):
        """
        Create two users with the same email.
        """
        create_user()
        try:
            create_user(username="otheruser")
            self.fail('Two users saved')
        except IntegrityError:
            pass

    def test_create_user_with_duplicate_username(self):
        """
        Create two users with the same username.
        """
        create_user()
        try:
            create_user(email="other@example.com")
            self.fail('Two users saved')
        except IntegrityError:
            pass

    def test_count_users_created(self):
        """
        Create many user and check number of users.
        """
        self.assertEqual(get_user_model().objects.count(), 0)
        create_user()
        self.assertEqual(get_user_model().objects.count(), 1)
        create_user(username="username1", email="user1@example.com")
        self.assertEqual(get_user_model().objects.count(), 2)
        create_user(username="username2", email="user2@example.com")
        self.assertEqual(get_user_model().objects.count(), 3)
