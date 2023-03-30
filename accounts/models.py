from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
import os


def get_profile_picture_path(instance, filename):
    return f'users/{instance.id}/profile_picture.jpg'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=127, blank=False, null=False, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    about = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(blank=True, upload_to=get_profile_picture_path, default='default/profile_picture.jpg')
    friends = models.ManyToManyField('User', blank=True, related_name='friends_set')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_friend_request', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user_friend_request', on_delete=models.CASCADE)


@receiver(pre_delete, sender=User)
def delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture and instance.profile_picture != 'default/profile_picture.jpg':
        picture_path = os.path.join(settings.MEDIA_ROOT, str(instance.profile_picture))
        os.remove(picture_path)


@receiver(pre_save, sender=User)
def delete_old_profile_picture(sender, instance, **kwargs):
    if instance.id:
        old_picture = sender.objects.get(id=instance.id).profile_picture
        if old_picture and old_picture != instance.profile_picture and old_picture != 'default/profile_picture.jpg':
            try:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(old_picture))
                os.remove(old_picture_path)
            except:
                pass