from lpn_notifications.models import Notification
from games.utils.igdb import get_igdb_data

def notify_friend(friend, message):
    notification = Notification(recipient=friend, message=message, url='invites_list')
    notification.save()


def notify_sender(sender, message):
    notification = Notification(recipient=sender, message=message, url='invites_list')
    notification.save()


def get_games(request, invites):
    for invite in invites:
        data=f'fields id,name,cover.url; where id = {invite.game};'
        game = get_igdb_data(request, data)
        invite.game = game[0]
    return invites


def get_game_name(request, game_id):
    data=f'fields name; where id = {game_id};'
    return get_igdb_data(request, data)[0]['name']

