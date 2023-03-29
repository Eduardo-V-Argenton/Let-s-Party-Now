from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users_list'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('friends/', views.friends, name='friends'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('send_friend_request/<str:username>', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove_friend/<str:username>', views.remove_friend, name='remove_friend'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('confirm_delete/', views.confirm_delete, name='confirm_delete'),
]
