from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib import messages


@login_required(redirect_field_name='login')
def notifications(request):
    notifications = Notification.objects.order_by('-send_date').filter(recipient=request.user)
    return render(request, 'lpn_notification/index.html', {'notifications':notifications})


@login_required(redirect_field_name='login')
def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    messages.info(request,'Notificação Excluída')
    return redirect('notifications')