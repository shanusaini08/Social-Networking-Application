from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import FRIEND_REQUEST_STATUS

class CommonTimePicker(models.Model):
    """
    An abstract model that provides created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SocialMediaUser(AbstractUser, CommonTimePicker):
    """
    Custom user model extending AbstractUser.
    """
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.email})'

class FriendRequest(models.Model):
    """
    Model to handle friend requests between users.
    """
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=FRIEND_REQUEST_STATUS, default='P')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.get_status_display()})"

class FriendRequestLimit(models.Model):
    """
    Model to handle rate limiting of friend requests.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.request_count} requests"

    class Meta:
        unique_together = ('user', 'timestamp')
