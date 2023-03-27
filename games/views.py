from django.shortcuts import render, redirect
from .utils.igdb import get_igdb_data
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login')
def index(request):
    page_number = request.GET.get('page', 1)
    search = request.GET.get('search')
    games_per_page = 20
    offset = (int(page_number) - 1) * games_per_page
    if not search:
        data = f"fields id,name,cover.url; limit {games_per_page}; offset {offset};sort rating desc; where rating != null;"
    else:
        data = f'search "{search}";fields id,name,cover.url; limit {games_per_page}; offset {offset};'
    games = get_igdb_data(request, data)
    if games != -1:
        
        return render(request, 'games/index.html', {
            'games': games,
            'games_per_page': games_per_page,
            'page_number': int(page_number)
        })    
    else:
        return redirect('index')


@login_required(redirect_field_name='login')
def game_page(request, game_id):
    data=f'fields name,summary,first_release_date,genres.name,platforms.name,cover.url; where id = {game_id};'
    game = get_igdb_data(request, data)
    if game != -1:
        return render(request, 'games/game_page.html', {'game':game[0]})
    else:
        return redirect('index')