from django.db import models
from accounts.models import User
from django.utils import timezone


class Championship(models.Model):
    championship_name = models.CharField(max_length=255, blank=False)
    organizer = models.ForeignKey(User, related_name='organizer', on_delete=models.DO_NOTHING)
    players = models.ManyToManyField(User, blank=True, related_name='players_set')
    game = models.IntegerField(default=0, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=127, blank=True)
    info = models.TextField(blank=True)
    vacancies = models.IntegerField(default=0)
    use_default_entrance = models.BooleanField(default=True)
    players_num = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    champion_name = models.CharField(max_length=255, blank=True)