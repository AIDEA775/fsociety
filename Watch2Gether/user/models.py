from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length = 200)
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username

    def sendFriendshipRequest(self, user):
        request = FriendshipRequest(sender=self, receiver=user)
        request.save()

    def getFriendshipRequests(self):
        requests = FriendshipRequest.objects.filter(
            receiver = self, accepted = False, rejected = False)
        return requests

    def addFriend(self, user):
        self.friends.add(user)
        user.friends.add(self)


class FriendshipRequest(models.Model):
    receiver = models.ForeignKey(
        User, related_name='receiver', on_delete=models.CASCADE)

    sender = models.ForeignKey(
        User, related_name='sender', on_delete=models.CASCADE)

    sent_date = models.DateTimeField('date sent', default=timezone.now())
    accepted = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)

    def __str__(self):
        return "<SENDER:{} RECEIVER:{}>".format(self.sender, self.receiver)

    def accept(self):
        self.accepted = True
        self.save()

    def reject(self):
        self.rejected = True
        self.save()
