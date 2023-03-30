from django.shortcuts import render
from . models import Championship
from django.contrib import messages
from games.utils.igdb import get_igdb_data
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='login')
def create(request, game_id):
    if request.method == 'POST':
        championship_name = request.POST['championship_name']
        start_date = request.POST['start_date']
        is_public = 'is_public' in request.POST
        password = request.POST.get('password', '')
        info = request.POST.get('info', '')
        vacancies = int(request.POST.get('vacancies', 0))
        use_default_entrance = 'use_default_entrance' in request.POST

        championship = Championship(championship_name=championship_name, organizer=request.user,
                                    start_date=start_date, is_public=not is_public, password=password,
                                    info=info, vacancies=vacancies, game=game_id,
                                    use_default_entrance=use_default_entrance)
        championship.save()
        messages.success(request, 'Campeonato Criado')
        # redirect
    
    return render(request, 'championships/create.html')


@login_required(redirect_field_name='login')
def list_public(request):
    page_number = request.GET.get('page', 1)
    championships = Championship.objects.filter(is_public=True)
    total_championships = championships.count()
    championships_per_page = 20
    offset = (int(page_number) - 1) * championships_per_page

    if offset + championships_per_page < total_championships:
        has_next = True
    else:
        has_next = False
    championships = championships[offset:offset+championships_per_page]

    for championship in championships:
        data=f'fields name; where id = {championship.game};'
        game = get_igdb_data(request, data)
        championship.game = game[0]

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })
    
    
@login_required(redirect_field_name='login')
def list_public_by_game(request, game_id):
    page_number = request.GET.get('page', 1)
    championships = Championship.objects.filter(is_public=True).filter(game=game_id)
    total_championships = championships.count()
    championships_per_page = 20
    offset = (int(page_number) - 1) * championships_per_page

    if offset + championships_per_page < total_championships:
        has_next = True
    else:
        has_next = False
    championships = championships[offset:offset+championships_per_page]

    for championship in championships:
        data=f'fields name; where id = {game_id};'
        game = get_igdb_data(request, data)
        championship.game = game[0]

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })