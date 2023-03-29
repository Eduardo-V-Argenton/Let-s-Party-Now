from django.db import models
from accounts.models import User, FriendRequest
from invites.models import Invite
from django.utils import timezone

class Notification(models.Model):
    sender = None
    recipient = None
    send_date = None 
    message = None
    url = None
    object_linked = None

    class Meta:
        abstract = True
    
    def search_id(search):
        frn = FriendRequestNotification.objects.order_by('-id').filter(id=search)
        ivn = InviteNotification.objects.order_by('-id').filter(id=search)
        empty_qs = FriendRequestNotification.objects.none()
        return empty_qs.union(frn, ivn)

    def search_recipient(search):
        frn = FriendRequestNotification.objects.order_by('-id').filter(recipient=search)
        ivn = InviteNotification.objects.order_by('-id').filter(recipient=search)
        empty_qs = FriendRequestNotification.objects.none()
        return empty_qs.union(frn, ivn)


class FriendRequestNotification(models.Model):
    sender = models.ForeignKey(User, related_name='sender_frn', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_frn', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, default='Você recebeu uma solicitação de Amizade')
    url = models.CharField(max_length=255, default='friend_requests') 
    object_linked = models.ForeignKey(FriendRequest, related_name='object_linked_frn', on_delete=models.CASCADE)


class InviteNotification(models.Model):
    sender = models.ForeignKey(User, related_name='sender_inv', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_inv', on_delete=models.CASCADE)
    send_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, default='invites_list') 
    object_linked = models.ForeignKey(Invite, on_delete=models.CASCADE)