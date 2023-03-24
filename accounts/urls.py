from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('friends/<int:user_id>/', views.friends, name='friends'),
    path('friend_requests/<int:user_id>/', views.friend_requests, name='friend_requests'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
