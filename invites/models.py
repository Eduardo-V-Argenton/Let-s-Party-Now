from django.db import models
from django.utils import timezone
from accounts.models import User
from typing import Any
from datetime import datetime


class Invite(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_invite', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user_invite', on_delete=models.CASCADE)
    game = models.IntegerField(default=0, blank=False)
    date = models.DateTimeField(default=timezone.now)
    message = models.TextField(default=None, blank=True)
    answered = models.BooleanField(default=False)
    answered_date = models.DateTimeField(default=timezone.now)
    was_accepted = models.BooleanField(default=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)





