from django.db import models
from django.utils import timezone
from django.conf import settings


class Friendship(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    # ManyToManyField is assumed to be symmetrical
    friends = models.ManyToManyField("self")

    def get_friends(self):
        return self.friends.all()

    def get_pending_requests(self, from_user=None):
        result = FriendshipRequest.objects.filter(
                receiver=self, status=FriendshipRequest.PENDING)

        if from_user:
            result.filter(sender=from_user)

        return result

    def send_request(self, user):
        if user not in self.get_friends() \
                and not user.get_pending_requests(from_user=self):
            FriendshipRequest.objects.create(sender=self, receiver=user)

    def add_friend(self, user):
        self.friends.add(user)

    def __str__(self):
        return "Friendship data from {}.".format(self.user.username)


class FriendshipRequest(models.Model):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

    STATUS = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    receiver = models.ForeignKey(
        Friendship, related_name='receiver', on_delete=models.CASCADE)

    sender = models.ForeignKey(
        Friendship, related_name='sender', on_delete=models.CASCADE)

    sent_date = models.DateTimeField('date sent', default=timezone.now)

    status = models.IntegerField(choices=STATUS, default=PENDING)

    def __str__(self):
        return "<SENDER:{} RECEIVER:{}>".format(self.sender.user.username,
                                                self.receiver.user.username)

    def accept(self):
        self.receiver.add_friend(self.sender)
        self.status = self.ACCEPTED
        self.save()

    def reject(self):
        self.status = self.REJECTED
        self.save()
