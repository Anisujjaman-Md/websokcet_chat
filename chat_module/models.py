from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content}'


class Room(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)


from django.db import models
from django.conf import settings


class ConnectionHistory(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    STATUS = (
        (ONLINE, 'On-line'),
        (OFFLINE, 'Off-line'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    device_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS,
        default=ONLINE
    )
    first_login = models.DateTimeField(auto_now_add=True)
    last_echo = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "device_id"),)
