from django.shortcuts import render, redirect
from django.contrib import messages
from .utils.igdb import get_igdb_data

def index(request):
    data = "fields name,cover.url; limit 10; sort rating desc;"
    games = get_igdb_data(request, data)
    if games != -1:
        return render(request, 'games/index.html', {'games':games})
    else:
        return redirect('index')

def search_game(request, name):
    data = f'search "{name}"; fields name,cover.url; limit 20;'
    games = get_igdb_data(request, data)
    if games != -1:
        return render(request, 'games/index.html', {'games':games})
    else:
        return redirect('index')