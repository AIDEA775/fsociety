from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Friendship

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_user_friendship(sender, instance, created, **kwargs):
    if created:
        Friendship.objects.create(user = instance)
