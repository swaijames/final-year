from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'form/signup.html')


def signin(request):
    return render(request, 'form/signin.html')


def forgot(request):
    return render(request, 'form/forgot.html')


def movie(request):
    return render(request, 'movie.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

        messages = '''
           New messages: {}

           from: {}
             '''.format(data['message'], data['email'])
        send_mail(data['subject'], messages, '', ['swahilisinema@gmail.com'])
    return render(request, 'contact.html')


def movie_details(request):
    return render(request, 'movie-details.html')
# Create your views here.
