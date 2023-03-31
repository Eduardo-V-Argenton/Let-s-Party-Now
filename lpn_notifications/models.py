from django.db import models
from accounts.models import User
from django.utils import timezone


class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    url = models.CharField(max_length=255) 