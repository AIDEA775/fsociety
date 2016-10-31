from django.test import TestCase, Client
from django.urls import reverse
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


class LoginUserModelTest(TestCase):
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
        self.assertRaises(IntegrityError, create_user, username="otheruser")

    def test_create_user_with_duplicate_username(self):
        """
        Create two users with the same username.
        """
        create_user()
        self.assertRaises(IntegrityError, create_user, email="other@example.com")

    def test_count_users_created(self):
        """
        Create many user and check number of users.
        """
        self.assertEqual(get_user_model().objects.count(), 0)
        create_user()
        self.assertEqual(get_user_model().objects.count(), 1)
        create_user(username="username1", email="user1@example.com")
        self.assertEqual(get_user_model().objects.count(), 2)


class LoginUserViewTest(TestCase):
    def test_create_user_with_invalid_email(self):
        form = {'email' : 'bademail',
        'password' : 'pass',
        'first_name' : 'Alice',
        'last_name' : 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'The email address is not valid')

    def test_create_user_with_empty_email(self):
        form = {'email' : '',
        'password' : 'pass',
        'first_name' : 'Alice',
        'last_name' : 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'The email address is not valid')

    def test_view_create_user_with_invalid_email(self):
        create_user(email='alice@example.com')
        form = {'email' : 'alice@example.com',
        'password' : 'pass',
        'first_name' : 'Alice',
        'last_name' : 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'Email is already in use')

    def test_create_user_with_empty_frist_name(self):
        form = {'email' : 'alice@example.com',
        'password' : 'pass',
        'first_name' : '',
        'last_name' : 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'A field is empty')

    def test_create_user_without_frist_name(self):
        form = {'email' : 'alice@example.com',
        'password' : 'pass',
        'last_name' : 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'A field is empty')

    def test_view_bad_login_user(self):
        form = {'username' : 'baduser',
                'password' : 'badpass'}
        response = self.client.post(reverse('login:login'), form)
        self.assertContains(response, 'Wrong username or password')
