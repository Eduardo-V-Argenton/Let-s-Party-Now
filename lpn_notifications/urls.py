from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('delete_notification/<int:notification_id>', views.delete_notification, name='delete_notification'),
]
