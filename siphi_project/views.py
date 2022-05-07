from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from .forms import UserCreationForm


# from .filters import OrderFilter


def index(request):
    return render(request, 'index.html')


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
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

        messager = '''
           New messages: {}

           from: {}
             '''.format(data['message'], data['email'])
        send_mail(data['subject'], messager, '', ['swahilisinema@gmail.com'])
        messages.success(request, "data sent to email")
    return render(request, 'contact.html')


def movie_details(request):
    return render(request, 'movie-details.html')
# Create your views here.
