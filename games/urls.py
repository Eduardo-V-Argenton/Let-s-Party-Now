from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='game_list'),
    path('search/<str:name>', views.search_game, name='search_game')   
]
