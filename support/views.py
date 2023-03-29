from django.shortcuts import render, redirect
from .models import SupportTicket
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def get_support(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        problem = request.POST.get('problem')

        st = SupportTicket(username = username, email=email,   
                           problem=problem)
        st.save()
        messages.success(request, 'Ticket de suporte enviado, aguarde '\
                         'que entraremos em contato por email')

        return redirect('index')
    else:
        return render(request, 'support/get_support.html')


@login_required(redirect_field_name='login')
def support_list(request):
    if request.user.is_staff:
        sts = SupportTicket.objects.all()
        return render(request, 'support/support_list.html', {'tickets':sts})
    else:
        return redirect('index')


@login_required(redirect_field_name='login')
def delete_ticket(request, ticket_id):
    if request.user.is_staff:
        sts = SupportTicket.objects.get(id=ticket_id)
        sts.delete()
        return redirect('support_list')
    else:
        return redirect('index')