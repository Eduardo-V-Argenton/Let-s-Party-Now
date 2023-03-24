from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from .models import User, FriendRequest


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not username or not email or not password or not password2:
        messages.error(request, 'Nenhum campo pode ficar vazio')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email Inválido')
        return render(request, 'accounts/register.html')
    if len(password) < 6:
        messages.error(request, 'Senha muito curta')
        return render(request, 'accounts/register.html')

    if len(username) < 6:
        messages.error(request, 'Usuário muito curto')
        return render(request, 'accounts/register.html')
    
    if password != password2:
        messages.error(request, 'Senhas Diferentes')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe')
        return render(request, 'accounts/register.html')
    
    user = User.objects.create_user(username=username, email=email, password=password, name=name)
    user.save()
    messages.success(request, 'Usuário Cadastrado')
    return redirect('login')


@login_required(redirect_field_name='login')
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if  request.user.friends.filter(id=user_id).exists():
        is_friend = True
    else:
        is_friend = False 

    return render(request, 'accounts/profile.html', {'user_profile':user, 'is_friend':is_friend})


@login_required(redirect_field_name='login')
def friends(request, user_id):
    if user_id is not request.user.id:
        return redirect('index')
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/friends.html', {'user':user})


@login_required(redirect_field_name='login')
def friend_requests(request, user_id):
    if user_id is not request.user.id:
        return redirect('index')
    friend_requests = FriendRequest.objects.order_by('-id').filter(to_user=user_id) 
    return render(request, 'accounts/friend_requests.html', {'friend_requests':friend_requests})


@login_required(redirect_field_name='login')
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    friend_request, created =  FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        messages.info(request,'Solicitação de amizade enviada')
    else:
        messages.error(request, 'Solicitação já enviada')
    return redirect('profile', to_user.id)
 

@login_required(redirect_field_name='login')
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.info(request,'Solicitação de amizade aceita')
    else:
        messages.info(request,'Solicitação de amizade não aceita')
    return redirect('friend_requests', request.user.id)


@login_required(redirect_field_name='login')
def reject_friend_request(request, request_id):
    if friend_request.to_user == request.user:
        friend_request = FriendRequest.objects.get(id=request_id)
        friend_request.delete()
        messages.info(request, 'Solicitação de amizade excluída')
    else:
        messages.error(request,'Solicitação de amizade não excluída')
    return redirect('friend_requests', request.user.id)


@login_required(redirect_field_name='login')
def remove_friend(request, user_id):
    if request.user.friends.filter(id=user_id).exists():
        user = get_object_or_404(User, id=user_id)
        user.friends.remove(request.user)
        request.user.friends.remove(user)
        messages.info(request,'Amigo Removido')
    else:
        messages.error(request,'Ocorreu um erro na remoção da amizade')
    return redirect('friends', request.user.id)