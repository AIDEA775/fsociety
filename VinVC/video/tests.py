from django.test import TestCase, Client
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse

from user.tests import create_two_users, friends
from login.tests import create_user, login_user


def upload_a_video(client, path='login/static/login/video/bg.mp4',
                   title='My video', description='My description'):
    """
    Upload a video as client and return response
    """
    with open(path, 'rb') as video:
        return client.post(reverse('video:upload'),
                           {'title': title,
                            'description': description,
                            'video_file': video})


class VideoTestsBase(TestCase):
    def setUp(self):
        """
        Create and login 3 users: User, Alice, Bob.
        Alice and bob are friends.
        """
        self.user = create_user()
        self.alice, self.bob = create_two_users()
        self.client_u = login_user(self.user.username)
        self.client_a = login_user(self.alice.username)
        self.client_b = login_user(self.bob.username)
        friends(self.alice, self.bob)


class VideoUploadDeleteTest(VideoTestsBase):
    def test_upload_video(self):
        response = upload_a_video(self.client_u)
        self.assertNotContains(response, 'Video not supported')
        self.assertEqual(self.user.author.all().count(), 1)

    def test_delete_video(self):
        upload_a_video(self.client_u)
        video = self.user.author.all()[0]
        self.client_u.get(reverse('video:delete'), {'id': video.id})
        self.assertEqual(self.user.author.all().count(), 0)

    def test_delete_video_of_other_user(self):
        upload_a_video(self.client_a)
        video = self.alice.author.all()[0]
        self.client_b.get(reverse('video:delete'), {'id': video.id})
        self.assertEqual(self.alice.author.all().count(), 1)

    def test_upload_video_without_title(self):
        upload_a_video(self.client_u, title='')
        self.assertEqual(self.user.author.all().count(), 0)


class VideoViewTest(VideoTestsBase):
    def setUp(self):
        """
        Alice have one video uploaded
        """
        super().setUp()
        upload_a_video(self.client_a)

    def test_view_uploaded(self):
        response = self.client_a.get(reverse('user:uploaded', kwargs={'user_id': self.alice.id}))
        self.assertEqual(response.context['videos'].count(), 1)

    def test_view_uploaded_without_videos(self):
        response = self.client_u.get(reverse('user:uploaded', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.context['videos'].count(), 0)

    def test_count_friends_videos(self):
        response = self.client_b.get(reverse('video:friends_videos'))
        self.assertEqual(response.context['videos'].count(), 1)

    def test_count_friends_videos_without_friends(self):
        response = self.client_u.get(reverse('video:friends_videos'))
        self.assertEqual(response.context['videos'].count(), 0)
