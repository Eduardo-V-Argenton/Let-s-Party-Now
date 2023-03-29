from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_support, name='get_support'),
    path('list/', views.support_list, name='support_list'),
    path('delete/<int:ticket_id>', views.delete_ticket, name='delete_ticket'),
]
