from django.db import models
from django.utils import timezone
from django.conf import settings


class Friendship(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    friends = models.ManyToManyField("self")

    def sendFriendshipRequest(self, user):
        request = FriendshipRequest(sender = self, receiver = user)
        request.save()

    def getFriendshipRequests(self):
        requests = FriendshipRequest.objects.filter(
            receiver = self, accepted = False, rejected = False)
        return requests

    def addFriend(self, user):
        self.friends.add(user)

    def __str__(self):
        return "Friendship data from {}.".format(self.user.username)


class FriendshipRequest(models.Model):
    receiver = models.ForeignKey(
        Friendship, related_name='receiver', on_delete = models.CASCADE)

    sender = models.ForeignKey(
        Friendship, related_name='sender', on_delete = models.CASCADE)

    sent_date = models.DateTimeField('date sent', default = timezone.now)
    accepted = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)

    def __str__(self):
        return "<SENDER:{} RECEIVER:{}>".format(self.sender.user.username,
                                                self.receiver.user.username)

    def accept(self):
        self.receiver.addFriend(self.sender)
        self.accepted = True
        self.save()

    def reject(self):
        self.rejected = True
        self.save()
