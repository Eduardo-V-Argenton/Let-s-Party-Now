from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from games.utils.igdb import get_igdb_data
from .models import Invite
from accounts.models import User
from .functions.functions import notify_friend, notify_sender, get_games, get_game_name


@login_required(redirect_field_name='login')
def index(request):
    invites = Invite.objects.order_by('-id').filter(to_user=request.user)
    invites = get_games(request, invites)
    return render(request, 'invites/index.html', {'invites':invites})


@login_required(redirect_field_name='login')
def create_invite(request, game_id):
    if request.method == 'POST':
        friends_ids = request.POST.getlist('friends')
        date = request.POST.get('datetime')
        message = request.POST.get('message')
        
        game_name = get_game_name(request, game_id)
        
        friends = User.objects.filter(id__in=friends_ids)
        for friend in friends:
            invite, created = Invite.objects.get_or_create(from_user=request.user, to_user=friend, \
                                           date=date, message=message, game=game_id)
            if created:
                notify_friend(friend, f'Você recebeu um convite de {request.user} para jogar {game_name}')
            else:
                messages.error(request, 'Erro ao enviar os convites')
                return redirect('create_invite', game_id)
        messages.info(request, 'Convites Enviado com sucessos')
        return redirect('game_page', game_id)
    else:
        friends = request.user.friends.all()
        date_time = timezone.localtime().strftime('%Y-%m-%dT%H:%M')
        return render(request, 'invites/create_invite.html', {
            'friends': friends,
            'default_datetime': date_time
        })

@login_required(redirect_field_name='login')
def accept_invite(request, invite_id): 
    invite = Invite.objects.get(id=invite_id)
    if not invite.answered:
        invite.answered = True
        invite.answered_date = timezone.now()
        invite.was_accepted = True
        invite.save()

        game_name = get_game_name(request, invite.game)
        
        notify_sender(invite.from_user, f'{request.user.username} aceitou seu pedido para jogar {game_name}')
        messages.success(request, 'Convite aceito')
    else:
        messages.error(request, 'Ocorreu um erro na aceitação do convite')
    return redirect('invites_list')


@login_required(redirect_field_name='login')
def reject_invite(request, invite_id):
    
    invite = Invite.objects.get(id=invite_id)
    if not invite.answered:
        invite.answered = True
        invite.answered_date = timezone.now()
        invite.was_accepted = False
        invite.save()

        game_name = get_game_name(request, invite.game)
        
        notify_sender(invite.from_user, f'{request.user.username} recusou seu pedido para jogar {game_name}')
        messages.success(request, 'Convite Recusado')
    else:
        messages.error(request, 'Ocorreu um erro na recusa do convite')
    return redirect('invites_list')

@login_required(redirect_field_name='login')
def delete_invite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    if invite.to_user == request.user:
        invite.delete()
        messages.success(request, 'Convite excluído')
    else:
        messages.error(request,'Convite não excluído')
    return redirect('invites_list')