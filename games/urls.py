from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.index, name='games_list'),
    path('<int:game_id>/', views.game_page, name='game_page'),
]
