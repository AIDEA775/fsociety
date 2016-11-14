from django.apps import AppConfig


class FriendshipConfig(AppConfig):
    name = 'friendship'

    def ready(self):
        import friendship.signals
