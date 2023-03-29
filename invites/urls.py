from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='invites_list'),
    path('create_invite/<int:game_id>', views.create_invite, name='create_invite'),
    path('accept_invite/<int:invite_id>', views.accept_invite, name='accept_invite'),
    path('reject_invite/<int:invite_id>', views.reject_invite, name='reject_invite'),
    path('delete_invite/<int:invite_id>', views.delete_invite, name='delete_invite'),
]
