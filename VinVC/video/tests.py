from django.test import TestCase, Client
from django.contrib.auth import get_user
from django.urls import reverse
from friendship.tests import UserFriendshipTest


def upload_video(client, path='login/static/login/video/bg.mp4',
                 title='My video', description='My description'):
    with open(path, 'rb') as video:
        context = {'title': title,
                   'description': description,
                   'video_file': video}
        return client.post(reverse('video:upload'), context)


class VideoTests(UserFriendshipTest):

    def setUp(self):
        super().setUp()
        self.user = self.create_user()
        self.client_a = self.login_user(self.alice.username)
        self.client_b = self.login_user(self.bob.username)
        self.client_u = self.login_user(self.user.username)
        self.friends(self.alice, self.bob)


class VideoUploadDeleteTest(VideoTests):
    def test_upload_video(self):
        response = upload_video(self.client_u)
        self.assertNotContains(response, 'Video not supported')
        self.assertEqual(self.user.video_set.all().count(), 1)

    def test_delete_video(self):
        upload_video(self.client_u)
        video = self.user.video_set.all()[0]
        self.client_u.get(reverse('video:delete'), {'id': video.id})
        self.assertEqual(self.user.video_set.all().count(), 0)

    def test_delete_video_of_other_user(self):
        upload_video(self.client_a)
        video = self.alice.video_set.all()[0]
        self.client_b.get(reverse('video:delete'), {'id': video.id})
        self.assertEqual(self.alice.video_set.all().count(), 1)

    def test_upload_video_without_title(self):
        upload_video(self.client_u, title='')
        self.assertEqual(self.user.video_set.all().count(), 0)


class VideoViewTest(VideoTests):
    def setUp(self):
        super().setUp()
        upload_video(self.client_a)

    def notest_view_uploaded(self):
        response = self.client_a.get(reverse('user:uploaded',
                                     kwargs={'user_id': self.alice.id}))
        self.assertEqual(response.context['videos'].count(), 1)

    def notest_view_uploaded_without_videos(self):
        response = self.client_u.get(reverse('user:uploaded',
                                     kwargs={'user_id': self.user.id}))
        self.assertEqual(response.context['videos'].count(), 0)

    def nonotest_count_friends_videos(self):
        response = self.client_b.get(reverse('video:friends_videos'))
        self.assertEqual(response.context['videos'].count(), 1)

    def notest_count_friends_videos_without_friends(self):
        response = self.client_u.get(reverse('video:friends_videos'))
        self.assertEqual(response.context['videos'].count(), 0)
