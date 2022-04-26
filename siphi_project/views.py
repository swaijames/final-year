from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def movie(request):
    return render(request, 'movie.html')


def contact(request):
    if request.method == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        messages = request.POST.get('messages')

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': messages
        }
        print(data)
        message = '''
        New message:{}
        
        from {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['rodgersswai69@gmail.com'])
        return HttpResponse('thank you')
    return render(request, 'contact.html', {})


def movie_details(request):
    return render(request, 'movie-details.html')
# Create your views here.
