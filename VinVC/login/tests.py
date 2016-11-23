from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user, get_user_model


class LoginUserTest(TestCase):

    def create_user(self, username="username", email="user@example.com",
                    password="pass", first_name="first", last_name="last"):
        return get_user_model().objects.create_user(username, email, password,
                                                    first_name=first_name,
                                                    last_name=last_name)

    def login_user(self, username="username", password="pass"):
        c = Client()
        c.login(username=username, password=password)
        return c


class LoginUserModelsTest(LoginUserTest):

    def test_login_user_authenticated(self):
        self.create_user()
        self.client = self.login_user()
        user = get_user(self.client)
        assert user.is_authenticated()

    def test_bad_login_user(self):
        self.create_user()
        self.client = self.login_user(password="badpass")
        user = get_user(self.client)
        assert not user.is_authenticated()


class LoginUserViewsTest(LoginUserTest):
    def test_create_user_with_invalid_email(self):
        form = {'email': 'bademail',
                'password': 'pass',
                'first_name': 'Alice',
                'last_name': 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'The email address is not valid')

    def test_create_user_with_empty_email(self):
        form = {'email': '',
                'password': 'pass',
                'first_name': 'Alice',
                'last_name': 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'The email address is not valid')

    def test_create_user_with_duplicate_email(self):
        self.create_user(email='alice@example.com')
        form = {'email': 'alice@example.com',
                'password': 'pass',
                'first_name': 'Alice',
                'last_name': 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'Email is already in use')

    def test_create_user_with_empty_frist_name(self):
        form = {'email': 'alice@example.com',
                'password': 'pass',
                'first_name': '',
                'last_name': 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'A field is empty')

    def test_create_user_without_frist_name(self):
        form = {'email': 'alice@example.com',
                'password': 'pass',
                'last_name': 'Henderson'}
        response = self.client.post(reverse('login:signup'), form)
        self.assertContains(response, 'A field is empty')

    def test_bad_login_user(self):
        form = {'username': 'baduser',
                'password': 'badpass'}
        response = self.client.post(reverse('login:login'), form)
        self.assertContains(response, 'Wrong username or password')
