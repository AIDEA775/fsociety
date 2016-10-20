from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    A custom user model with unique email field
    """
    email = models.CharField(max_length=40, unique=True, blank=False)
