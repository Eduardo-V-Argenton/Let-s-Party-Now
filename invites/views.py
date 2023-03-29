from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from games.utils.igdb import get_igdb_data
from .models import Invite
from lpn_notifications.models import InviteNotification
from accounts.models import User


@login_required(redirect_field_name='login')
def index(request):
    invites = Invite.objects.order_by('-id').filter(to_user=request.user)
    for invite in invites:
        data=f'fields id,name,cover.url; where id = {invite.game};'
        game = get_igdb_data(request, data)
        invite.game = game[0]
    return render(request, 'invites/index.html', {'invites':invites})


@login_required(redirect_field_name='login')
def create_invite(request, game_id):
    if request.method == 'POST':
        friends_ids = request.POST.getlist('friends')
        date = request.POST.get('datetime')
        message = request.POST.get('message')
        
        data=f'fields name; where id = {game_id};'
        game_name = get_igdb_data(request, data)[0]['name']
        
        friends = User.objects.filter(id__in=friends_ids)
        for friend in friends:
            invite, created = Invite.objects.get_or_create(from_user=request.user, to_user=friend, \
                                           date=date, message=message, game=game_id)
            if created:
                ivn, created = InviteNotification.objects.get_or_create(sender=request.user, \
                        recipient=friend, object_linked=invite, \
                            message=f'Você recebeu um convite de {request.user}'\
                                f' para jogar {game_name}')
                if not created:
                    messages.error(request, 'Erro Aqui mermão')
                ivn.save()
            else:
                messages.error(request, 'Erro ao enviar os convites')
                return redirect('index')
        messages.info(request, 'Convites Enviado com sucessos')
        return redirect('index')
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

        data=f'fields name; where id = {invite.game};'
        game_name = get_igdb_data(request, data)[0]['name']
        
        ivn = InviteNotification.objects.create(sender=request.user, \
                recipient=invite.from_user, object_linked=invite, \
                    message=f'{request.user.username} aceitou seu pedido para jogar {game_name}')
        ivn.save()
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

        data=f'fields name; where id = {invite.game};'
        game_name = get_igdb_data(request, data)[0]['name']
        
        ivn = InviteNotification.objects.create(sender=request.user, \
                recipient=invite.from_user, object_linked=invite, \
                    message=f'{request.user.username} recusou seu pedido para jogar {game_name}')
        ivn.save()
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