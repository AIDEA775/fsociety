from django.db import models
from django.contrib.auth.models import AbstractUser

def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/<username>.jpg
    return 'avatars/{}.jpg'.format(instance.username)

class CustomUser(AbstractUser):
    """
    A custom user model with unique email field
    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to=avatar_directory_path,
                               default='avatars/placeholder.jpg')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
