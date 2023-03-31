from ..models import Championship
from games.utils.igdb import get_igdb_data
from django.contrib import messages
from lpn_notifications.models import Notification


def get_game(request,championships, game_id=None):
    for championship in championships:
        data=f'fields name,cover.url; where id = {game_id if game_id else championship.game};'
        game = get_igdb_data(request, data)
        championship.game = game[0]
    return championships


def build_pagination(request, game_id=None, organizer=None, players=None):
    page_number = request.GET.get('page', 1)
    if game_id:
        championships = Championship.objects.filter(is_public=True).filter(game=game_id)
    elif organizer:
        championships = Championship.objects.filter(organizer=organizer)
    elif players:
        championships = Championship.objects.filter(players=request.user)
    else:
        championships = Championship.objects.filter(is_public=True)

    total_championships = championships.count()
    championships_per_page = 20
    offset = (int(page_number) - 1) * championships_per_page

    if offset + championships_per_page < total_championships:
        has_next = True
    else:
        has_next = False
    championships = championships[offset:offset+championships_per_page]

    championships = get_game(request, championships, game_id)
    return championships, has_next, page_number


def validate_edit(request, championship):
    start_date = request.POST['start_date']
    password = request.POST.get('password', '')
    info = request.POST.get('info', '')
    vacancies = request.POST.get('vacancies', '')
    players_num = request.POST.get('players_num', '')

    if start_date and start_date != championship.start_date:
        championship.start_date = start_date
    if password and not championship.is_public and password != championship.password:
        championship.password = password
    if info and info != championship.info:
        championship.info = info
    if vacancies and int(vacancies) != championship.vacancies:
        if (championship.use_default_entrance and championship.players.count() < int(vacancies)) or \
                (not championship.use_default_entrance and championship.players_num < int(vacancies)):
            championship.vacancies = int(vacancies)
        else:
            messages.error(request, 'O número de vagas não pode ser maior que o número participantes')
    if players_num and int(players_num) <= championship.vacancies and \
            not championship.use_default_entrance and int(players_num) != championship.players_num:
        championship.players_num = int(players_num)
    else:

        messages.error(request, 'O número de jogadores não pode ser maior do que o de vagas')
    return championship


def validate_delete(request, championship):
    if championship.players.count() > 25:
        if not championship.use_default_entrance and championship.players_num \
                >= 0.75 * championship.vacancies:
            messages.error(request, 'O campeonato não pode ser excluído, entre em contato com o suporte')
            return False
        elif championship.use_default_entrance and championship.players.count() \
                >= 0.75 * championship.vacancies:
            messages.error(request, 'O campeonato não pode ser excluído, entre em contato com o suporte')
            return False
    return True


def notify_all_players(players, message):
    for player in players.all():
        notification = Notification(recipient=player, message=message, url='championships_list_participating')
        notification.save()


def notify_organizer(organizer, message):
    notification = Notification(recipient=organizer, message=message, url='my_championships_list')
    notification.save()


def notify_player(player, message):
    notification = Notification(recipient=player, message=message, url='championships_list_participating')
    notification.save()