from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import RequestDataTooBig
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.db.models import Q
from .models import User, FriendRequest
from lpn_notifications.models import FriendRequestNotification


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
def index(request):
    page_number = request.GET.get('page', 1)
    search_users_per_page = 20
    offset = (int(page_number) - 1) * search_users_per_page
    search = request.GET.get('search')
    if search:
        users = User.objects.filter(Q(name__icontains=search) | Q(username__icontains=search))
        search_users_total = users.count()
        if offset + search_users_per_page < search_users_total:
            has_next = True
        else:
            has_next = False 
        users = users[offset:offset + search_users_per_page] 
    else:
        users = User.objects.all
    return render(request, 'accounts/index.html', {
        'search_users': users,
        'has_next': has_next,
        'page_number': int(page_number),
    })    


@login_required(redirect_field_name='login')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if  request.user.friends.filter(username=username).exists():
        is_friend = True
    else:
        is_friend = False 

    return render(request, 'accounts/profile.html', {'user_profile':user, 'is_friend':is_friend})


@login_required(redirect_field_name='login')
def friends(request):
    return render(request, 'accounts/friends.html')


@login_required(redirect_field_name='login')
def friend_requests(request):
    friend_requests = FriendRequest.objects.order_by('-id').filter(to_user=request.user) 
    return render(request, 'accounts/friend_requests.html', {'friend_requests':friend_requests})


@login_required(redirect_field_name='login')
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    friend_request, created =  FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if created:
        frn = FriendRequestNotification.objects.create(sender=request.user, 
                            recipient=to_user, object_linked=friend_request)
        frn.save()
        messages.info(request,'Solicitação de amizade enviada')
    else:
        messages.error(request, 'Solicitação já enviada')
    return redirect('profile', username)
 

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
    return redirect('friend_requests')


@login_required(redirect_field_name='login')
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.info(request, 'Solicitação de amizade excluída')
    else:
        messages.error(request,'Solicitação de amizade não excluída')
    return redirect('friend_requests')


@login_required(redirect_field_name='login')
def remove_friend(request, username):
    if request.user.friends.filter(username=username).exists():
        user = get_object_or_404(User, username=username)
        user.friends.remove(request.user)
        request.user.friends.remove(user)
        messages.info(request,'Amigo Removido')
    else:
        messages.error(request,'Ocorreu um erro na remoção da amizade')
    return redirect('profile', username)


@login_required(redirect_field_name='login')
def edit_profile(request):
    try:

        if request.method != 'POST':
            image_too_large = request.GET.get('image_too_large')
            if(image_too_large == 'true'):
                raise RequestDataTooBig
            return render(request, 'accounts/edit_profile.html')

        name = request.POST.get('name')
        profile_picture = request.FILES.get('profile_picture')
        email = request.POST.get('email')
        about = request.POST.get('about')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        
        user = get_object_or_404(User, username=request.user.username)
        
        if len(name) == 0:
            messages.error(request, 'Nome não pode ser vazio')
            return render(request, 'accounts/edit_profile.html')
        elif user.name != name:
            user.name = name
        
        if profile_picture is not None:
            user.profile_picture = profile_picture
            
        if email != user.email:
            try:
                if len(email) == 0:
                    messages.error(request, 'Email não pode ser vazio')
                    return render(request, 'accounts/edit_profile.html')
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email já existe')
                    return render(request, 'accounts/edit_profile.html')
                user.email = email
            except:
                messages.error(request, 'Email Inválido')
                return render(request, 'accounts/edit_profile.html')
        
        user.about = about

        if len(password) > 0:
            if len(password) < 6:
                messages.error(request, 'Senha muito curta')
                return render(request, 'accounts/edit_profile.html')
            elif password != password2:
                messages.error(request, 'Senhas Diferentes')
                return render(request, 'accounts/edit_profile.html')
            else:
                user.set_password(password)

        user.save()

        messages.success(request, 'Alterações Salvas')
    except RequestDataTooBig:
        messages.error(request, 'Imagem muito grande, o tamanho máximo permitido é de 1.5MB')
        return redirect('edit_profile')
    
    return redirect('profile', request.user.username)

@login_required(redirect_field_name='login')
def delete_account(request):
    return render(request, 'accounts/delete_account.html')

@login_required(redirect_field_name='login')
def confirm_delete(request):
    user = get_object_or_404(User, username=request.user.username)
    user.delete()
    return redirect('login')