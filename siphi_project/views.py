from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
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
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exist!! please try some other username")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!! please try another email")
            return redirect('signup')
        if len(username) > 10:
            messages.error(request, "username too long must be less than 10 characters")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "password do not match!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "username must be alphanumeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "successfully signed up")

        # form = UserCreationForm()
        # if request.method == 'POST':
        #     form = UserCreationForm(request.POST)
        #     if form.is_valid():
        #         form.save()
        #
        # context = {'form': form}
        return redirect('signin')
    return render(request, 'form/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        paswrd = request.POST['password']

        user = authenticate(username=username, password=paswrd)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})
        else:
            messages.error(request, "bad credentials:")
            return redirect('signin')

    return render(request, 'form/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "successfully logout")
    return redirect('signin')


# def reset_password(request):
#     return render(request, 'form/forgot.html')


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
