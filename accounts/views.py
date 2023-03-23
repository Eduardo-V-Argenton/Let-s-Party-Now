from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from .models import User

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
def profile(request):
    return render(request, 'accounts/profile.html')
