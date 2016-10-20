from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from .models import CustomUser

def signup(username, email, password):
    CustomUser.objects.create_user(username, email, password)

class LoginUser(TestCase):
    def test_login_user_and_test_home_page(self):
        """
        Create new user an save this in database.
        """
        signup("username", "example@example", "password")
        self.client.login(username="username", password="password")
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Bienvenido")

    def test_signup_user_with_duplicate_email(self):
        """
        Create two user with the same email.
        """
        signup("username", "user@user.com", "password")
        try:
            signup("otheruser", "user@user.com", "password")
            self.fail('Two user saved!')
        except IntegrityError:
            pass

    def test_signup_user_with_duplicate_username(self):
        """
        Create two user with the same username.
        """
        signup("username", "user@user.com", "password")
        try:
            signup("username", "other@other.com", "password")
            self.fail('Two user saved!')
        except IntegrityError:
            pass
