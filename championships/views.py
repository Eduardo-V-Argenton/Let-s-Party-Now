from django.shortcuts import render, redirect
from . models import Championship,User
from .functions.functions import build_pagination, get_game, validate_edit, validate_delete, notify_all_players, notify_organizer, notify_player
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='login')
def create(request, game_id):
    if request.method == 'POST':
        championship_name = request.POST['championship_name']
        start_date = request.POST['start_date']
        is_public = 'is_public' in request.POST
        password = request.POST.get('password', '')
        info = request.POST.get('info', '')
        vacancies = request.POST.get('vacancies', 0)
        use_default_entrance = 'use_default_entrance' in request.POST

        championship = Championship(championship_name=championship_name, organizer=request.user,
                                    start_date=start_date, is_public=not is_public, password=password,
                                    info=info, vacancies=int(vacancies), game=game_id,
                                    use_default_entrance=use_default_entrance)
        championship.save()
        messages.success(request, 'Campeonato Criado')
        return redirect('championship_page', championship.id)
    
    return render(request, 'championships/create.html')


@login_required(redirect_field_name='login')
def list_public(request):
    championships,has_next, page_number = build_pagination(request)

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })
    
    
@login_required(redirect_field_name='login')
def list_public_by_game(request, game_id):
    championships,has_next, page_number = build_pagination(request, game_id=game_id)

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def championship_page(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    get_game(request, [championship])
    return render(request, 'championships/championship_page.html', {
        'championship':championship
    })
    

@login_required(redirect_field_name='login')
def edit(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.organizer == request.user:
        if request.method == 'POST':
            championship = validate_edit(request, championship)
            championship.save()
            messages.success(request, 'Campeonato Editado')
            notify_all_players(championship.players, f"O campeonato {championship.championship_name} teve modificações")
            return redirect('championship_page',championship_id)
        else:
            return render(request, 'championships/edit.html',{
                'championship':championship
        })
    redirect('index')


@login_required(redirect_field_name='enter_championship')
def enter_championship(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.use_default_entrance and request.user not in championship.players.all():
        if championship.is_public and championship.players.count() < championship.vacancies: 
            championship.players.add(request.user)
            championship.save()
            notify_organizer(championship.organizer, f"{request.user.username} entrou em {championship.championship_name}")
            return redirect('championship_page',championship_id)
    else:
        return redirect('public_championships')

@login_required(redirect_field_name='enter_championship')
def exit_championship(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.use_default_entrance and request.user in championship.players.all():
        championship.players.remove(request.user)
        championship.save()
        notify_organizer(championship.organizer, f"{request.user.username} saiu de {championship.championship_name}")
        return redirect('championship_page',championship_id)
    else:
        return redirect('public_championships')


@login_required(redirect_field_name='enter_championship')
def remove_player(request, championship_id, player_id):
    championship = Championship.objects.get(id=championship_id)
    player = User.objects.get(id=player_id)
    if championship.use_default_entrance and player in championship.players.all()\
            and championship.organizer == request.user:
        championship.players.remove(player)
        championship.save()
        notify_player(player, f"Você foi removido de {championship.championship_name}")
        return redirect('championship_page',championship_id)
    else:
        return redirect('public_championships')


@login_required(redirect_field_name='login')
def my_championships_list(request):
    championships,has_next, page_number = build_pagination(request, organizer=request.user)

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def championships_list_participating(request):
    championships,has_next, page_number = build_pagination(request, players=request.user)
    
    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def delete(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.organizer == request.user:
        can_delete = validate_delete(request, championship)
        if can_delete:
            if championship.use_default_entrance:
                notify_all_players(championship.players, f"O campeonato {championship.championship_name} foi excluído")
            championship.delete()
            messages.success(request, 'Campeonato Excluído')
    return redirect('index')