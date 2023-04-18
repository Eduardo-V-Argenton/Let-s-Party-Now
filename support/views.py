from django.shortcuts import render, redirect
from .models import SupportTicket, Review
from django.contrib import messages


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

def review(request):
    if request.method == 'POST':
        score = int(request.POST.get('score'))
        comment = request.POST.get('comment')

        if score and comment and score >= 0 and score <= 10:
            review = Review(score=score, comment=comment)
            review.save()
        else:
            messages.error(request,'A nota deve ser entre 0 e 10')
            return render(request, 'support/review.html')

        messages.success(request, 'Obrigado pela avaliação')
        return redirect('index')
    else:
        return render(request, 'support/review.html')