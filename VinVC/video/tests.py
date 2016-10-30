from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse

from user.tests import create_two_users
from login.tests import create_user, login_user


class VideoTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.alice, self.bob = create_two_users()

    def test_user_upload_video(self):
        self.client = login_user()
        with open('login/static/login/video/bg.mp4', 'rb') as video:
            self.client.post(reverse('video:upload'),
                {'title' : 'my video',
                 'description' : 'my description',
                 'video_file' : video})
        user = get_user(self.client)
        self.assertEqual(user.video_set.all().count(), 1)
