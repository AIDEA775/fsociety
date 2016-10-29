from django.db import models
from django.conf import settings

#from datetime import datetime
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from login.models import CustomUser
import urllib, hashlib, binascii


class Message(models.Model):
    user = models.CharField(max_length=200)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                            on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    gravatar = models.CharField(max_length=300)

    def __str__(self):
        return self.user


def generate_avatar(email):
    avatar = "http://www.gravatar.com/avatar/"
    avatar+=hashlib.md5(email.lower()).hexdigest()
    avatar+='?d=identicon'
    return avatar


def hash_username(username):
    hash_user = binascii.crc32(username)
    return hash_user


class ChatUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userID =  models.IntegerField()
    username = models.CharField(max_length=300)
    is_chat_user = models.BooleanField(default=False)
    gravatar_url = models.CharField(max_length=300)
    last_accessed = models.DateTimeField(auto_now_add=True)

CustomUser.profile = property(lambda u: ChatUser.objects.get_or_create(user=u, defaults={'gravatar_url':generate_avatar(u.email),'username':u.username,'userID':hash_username(u.username)})[0])

# a = ChatUser(user= "usertest", username="test", userID=12, gravatar_url="")
