from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:game_id>', views.create, name='create_championship'),
    path('', views.list_public, name='public_championships'),
    path('my_list/', views.my_championships_list, name='my_championships_list'),
    path('participating/', views.championships_list_participating, name='championships_list_participating'),
    path('public_list/game/<int:game_id>', views.list_public_by_game, name='public_championships_by_game'),
    path('<int:championship_id>/', views.championship_page, name='championship_page'),
    path('edit/<int:championship_id>/', views.edit, name='edit_championship'),
    path('enter_championship/<int:championship_id>', views.enter_championship, name="enter_championship"),
    path('exit_championship/<int:championship_id>', views.exit_championship, name="exit_championship"),
    path('remove_player/<int:championship_id><int:player_id>', views.remove_player, name="remove_player"),
    path('delete/<int:championship_id>', views.delete, name="delete_championship"),
]
