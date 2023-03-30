from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:game_id>', views.create, name='create_championship'),
    path('public_list/', views.list_public, name='public_championships'),
    path('public_list/game/<int:game_id>', views.list_public_by_game, name='public_championships_by_game'),
]
