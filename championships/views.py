from django.shortcuts import render, redirect
from . models import Championship,User
from django.contrib import messages
from games.utils.igdb import get_igdb_data
from lpn_notifications.models import ChampionshipNotification
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
        return redirect('championship_page', championship.id)
    
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
        data=f'fields name,cover.url; where id = {championship.game};'
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
        data=f'fields name,cover.url; where id = {game_id};'
        game = get_igdb_data(request, data)
        championship.game = game[0]

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def championship_page(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    data=f'fields name,cover.url; where id = {championship.game};'
    game = get_igdb_data(request, data)
    championship.game = game[0]
    return render(request, 'championships/championship_page.html', {
        'championship':championship
    })
    

@login_required(redirect_field_name='login')
def edit(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.organizer == request.user:
        if request.method == 'POST':
            start_date = request.POST['start_date']
            password = request.POST.get('password', '')
            info = request.POST.get('info', '')
            vacancies = int(request.POST.get('vacancies', ''))
            players_num = request.POST.get('players_num', '')
            if start_date and start_date != championship.start_date:
                championship.start_date = start_date
            if password and not championship.is_public and password != championship.password:
                championship.password = password
            if info and info != championship.info:
                championship.info = info
            if vacancies and vacancies != championship.vacancies:
                if championship.use_default_entrance and championship.players.count() < vacancies:
                    championship.vacancies = vacancies
                elif not championship.use_default_entrance and championship.players_num < vacancies:
                    championship.vacancies = vacancies
                else:
                    messages.error(request, 'O número de vagas não pode ser maior que o número participantes')
            if players_num and int(players_num) <= championship.vacancies and \
                    not championship.use_default_entrance and int(players_num) != championship.players_num:
                championship.players_num = int(players_num)
                messages.error(request, 'O número de jogadores não pode ser maior do que o de vagas')
            championship.save()
            messages.success(request, 'Campeonato Editado')
            for player in championship.players.all():
                chn = ChampionshipNotification(sender=request.user, recipient=player,
                                               message=f"O campeonato {championship.championship_name} teve modificações")
                chn.save()
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
            chn = ChampionshipNotification(sender=request.user, recipient=championship.organizer,
                                    message=f"{request.user.username} entrou em {championship.championship_name}")
            chn.save()
            return redirect('championship_page',championship_id)
        elif not championship.is_public and championship.players_num < championship.vacancies:   
            championship.players.add(request.user)
            championship.save()
            chn = ChampionshipNotification(sender=request.user, recipient=championship.organizer,
                                    message=f"{request.user.username} entrou em {championship.championship_name}")
            chn.save()
            return redirect('championship_page',championship_id)
    else:
        return redirect('public_championships')

@login_required(redirect_field_name='enter_championship')
def exit_championship(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.use_default_entrance and request.user in championship.players.all():
        championship.players.remove(request.user)
        championship.save()
        chn = ChampionshipNotification(sender=request.user, recipient=championship.organizer,
                                message=f"{request.user.username} saiu de {championship.championship_name}")
        chn.save()
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
        chn = ChampionshipNotification(sender=request.user, recipient=player, 
                                message=f"Você foi removido de {championship.championship_name}")
        chn.save()
        return redirect('championship_page',championship_id)
    else:
        return redirect('public_championships')


@login_required(redirect_field_name='login')
def my_championships_list(request):
    page_number = request.GET.get('page', 1)
    championships = Championship.objects.filter(organizer=request.user)
    total_championships = championships.count()
    championships_per_page = 20
    offset = (int(page_number) - 1) * championships_per_page

    if offset + championships_per_page < total_championships:
        has_next = True
    else:
        has_next = False
    championships = championships[offset:offset+championships_per_page]

    for championship in championships:
        data=f'fields name,cover.url; where id = {championship.game};'
        game = get_igdb_data(request, data)
        championship.game = game[0]

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def championships_list_participating(request):
    page_number = request.GET.get('page', 1)
    championships = Championship.objects.filter(players=request.user)
    total_championships = championships.count()
    championships_per_page = 20
    offset = (int(page_number) - 1) * championships_per_page

    if offset + championships_per_page < total_championships:
        has_next = True
    else:
        has_next = False
    championships = championships[offset:offset+championships_per_page]

    for championship in championships:
        data=f'fields name,cover.url; where id = {championship.game};'
        game = get_igdb_data(request, data)
        championship.game = game[0]

    return render(request, 'championships/index.html', {
        'championships':championships,
        'has_next': has_next,
        'page_number': int(page_number),
        })


@login_required(redirect_field_name='login')
def delete(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    if championship.organizer == request.user:
        if championship.players.count() > 25:
            if not championship.use_default_entrance and championship.players_num \
                    >= 0.75 * championship.vacancies:
                messages.error(request, 'O campeonato não pode ser excluído, entre em contato com o suporte')
            elif championship.use_default_entrance and championship.players.count() \
                    >= 0.75 * championship.vacancies:
                messages.error(request, 'O campeonato não pode ser excluído, entre em contato com o suporte')
            else:
                for player in championship.players.all():
                    chn = ChampionshipNotification(sender=request.user, recipient=player,
                                                message=f"O campeonato {championship.championship_name} foi excluído")
                    chn.save()
                championship.delete()
                messages.success(request, 'Campeonato Excluído')
        else:
            for player in championship.players.all():
                chn = ChampionshipNotification(sender=request.user, recipient=player,
                                               message=f"O campeonato {championship.championship_name} foi excluido")
                chn.save()
            championship.delete()
            messages.success(request, 'Campeonato Excluído')
    return redirect('index')