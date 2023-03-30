from django.db import models
import uuid
from accounts.models import User, FriendRequest
from invites.models import Invite
from championships.models import Championship
from django.utils import timezone


class CustomIDField(models.UUIDField):
    def __init__(self, **kwargs):
        kwargs.setdefault('default', uuid.uuid4)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        super().__init__(**kwargs)


class Notification(models.Model):
    sender = None
    recipient = None
    send_date = None 
    message = None
    url = None

    class Meta:
        abstract = True
    
    def search_recipient(search):
        frn = FriendRequestNotification.objects.order_by('-send_date').filter(recipient=search)
        ivn = InviteNotification.objects.order_by('-send_date').filter(recipient=search)
        chn = ChampionshipNotification.objects.order_by('-send_date').filter(recipient=search)
        empty_qs = FriendRequestNotification.objects.none()
        return empty_qs.union(frn, ivn, chn)

    def delete(id):
        frn = FriendRequestNotification.objects.filter(id=id)
        frn.delete()
        ivn = InviteNotification.objects.filter(id=id)
        ivn.delete()
        chn = ChampionshipNotification.objects.filter(id=id)
        chn.delete()

class FriendRequestNotification(models.Model):
    id = CustomIDField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sender_frn', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_frn', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, default='Você recebeu uma solicitação de Amizade')
    url = models.CharField(max_length=255, default='friend_requests') 


class InviteNotification(models.Model):
    id = CustomIDField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sender_inv', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_inv', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, default='invites_list') 


class ChampionshipNotification(models.Model):
    id = CustomIDField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sender_c', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_c', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, default='championships_list_participating') 