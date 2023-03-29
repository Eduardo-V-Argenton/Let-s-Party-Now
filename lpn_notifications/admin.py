from django.contrib import admin
from .models import FriendRequestNotification, InviteNotification
# Register your models here.

admin.site.register(FriendRequestNotification)
admin.site.register(InviteNotification)