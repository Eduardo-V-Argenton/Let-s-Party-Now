from django.db import models
from django.utils import timezone
from django.contrib import messages

class SupportTicket(models.Model):
    username = models.CharField(max_length=127, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    problem = models.TextField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)
    is_answered = models.BooleanField(default=False)

    