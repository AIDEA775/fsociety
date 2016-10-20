from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    A custom user model with unique email field
    """
    email = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=20, default=None)
    last_name = models.CharField(max_length=20, default=None)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
