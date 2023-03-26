from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .utils.igdb import get_igdb_data

def index(request):
    page_number = request.GET.get('page', 1)
    games_per_page = 20
    offset = (int(page_number) - 1) * games_per_page
    data = f"fields id,name,cover.url; limit {games_per_page}; offset {offset};sort rating desc; where rating != null;"
    games = get_igdb_data(request, data)
    if games != -1:
        
        return render(request, 'games/index.html', {
            'games': games,
            'games_per_page': games_per_page,
            'page_number': int(page_number)
        })    
    else:
        return redirect('index')

def search_game(request, name):
    data = f'search "{name}"; fields name,cover.url; limit 20;'
    games = get_igdb_data(request, data)
    if games != -1:
        return render(request, 'games/index.html', {'games':games})
    else:
        return redirect('index')

def game_page(request, game_id):
    data=f'fields name,summary,first_release_date,genres.name,platforms.name,cover.url; where id = {game_id};'
    game = get_igdb_data(request, data)
    if game != -1:
        return render(request, 'games/game_page.html', {'game':game[0]})
    else:
        return redirect('index')