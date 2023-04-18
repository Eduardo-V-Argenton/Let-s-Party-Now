from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_support, name='get_support'),
    path('review/', views.review, name='review'),
]
