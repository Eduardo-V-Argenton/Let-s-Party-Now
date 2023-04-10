from lpn_notifications.models import Notification
from django.contrib import messages
from ..models import User
from django.core.validators import validate_email
from django.core.exceptions import RequestDataTooBig


def friend_request_notification(to_user):
    notification = Notification.objects.create(recipient=to_user, \
                message="Você recebeu uma solicitação de amizade", url="friend_requests")
    notification.save()


def validate_user(request, name, email, password, password2, username=None, user = None):
    if not user:
        if not name or not username or not email or not password or not password2:
            messages.error(request, 'Nenhum campo pode ficar vazio')
            return False

    if email:
        try:
            validate_email(email)
        except:
            messages.error(request, 'Email inválido')
            return False

            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return False
    
    if password and len(password) < 6:
        messages.error(request, 'Senha muito curta')
        return False

    if username and len(username) < 6:
        messages.error(request, 'Usuário muito curto')
        return False
    
    if password and password2 and password != password2:
        messages.error(request, 'Senhas Diferentes')
        return False

    if not user:
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe')
            return False

    return True


def edit_values_modified(request, user, name, email, password, password2, profile_picture, about):
    validated = validate_user(request, name=name, email=email, password=password, password2=password2, user=user) 
    if validated:
        if profile_picture is not None:
            user.profile_picture = profile_picture
        
        if name and name != user.name:
            user.name = name
        
        if email and email != user.email:
            user.email = email
        
        if password:
            user.set_password(password)
        
        if about and about != user.about:
            user.about = about
        
        user.save()
        messages.success(request, 'Alterações Salvas')
            

def raise_image_too_large(request):
    image_too_large = request.GET.get('image_too_large')
    if(image_too_large == 'true'):
        raise RequestDataTooBig