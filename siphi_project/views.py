from profile import Profile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import uuid

from .models import *
from .forms import UserCreationForm


# from .filters import OrderFilter


def index(request):
    movies = MovieImage.objects.all().order_by('-uploaded')[:4]
    tprate = MovieImage.objects.all().order_by('movie__vote')[:4]
    Action = MovieImage.objects.all().filter(movie__category="A")[:4]
    Drama = MovieImage.objects.all().filter(movie__category="D")[:4]
    Comedy = MovieImage.objects.all().filter(movie__category="C")[:4]
    Horror = MovieImage.objects.all().filter(movie__category="H")[:4]
    return render(request, 'index.html',
                  {"tprate": tprate, "Action": Action, "Drama": Drama, "Comedy": Comedy, "Horror": Horror,
                   "movies": movies})


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
        if len(username) > 20:
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
    return redirect('index')


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
        send_mail(data['subject'], messager, '', ['pinchkiller@outlook.com'])
        messages.success(request, "data sent to email")
    return render(request, 'contact.html')


def movie_details(request):
    return render(request, 'movie-details.html')


def change_password(request, uid):
    try:
        if Profile.objects.filter(uuid=uid).exists():
            if request.method == 'POST':
                pass1 = 'password1' in request.POST and request.POST['password1']
                pass2 = 'password2' in request.POST and request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(uuid=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request, "password has been reset successfully")
                    return redirect('signin')
                else:
                    messages.error(request, "two password did not match")
        else:
            return HttpResponse('invalid url')
    except:
        return HttpResponse('invalid url')
    return render(request, './form/password_reset_confirm.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            url = f'http://127.0.0.1:8000/password_reset_confirm/{uid.profile.uuid}'
            send_mail('Reset password', url, settings.EMAIL_HOST_USER, [email], fail_silently=False, )
            return redirect('password_reset_done')
        else:
            messages.error(request, "email address is not exists")
    return render(request, './form/forgot.html')


def password_reset_done(request):
    return render(request, './form/password_reset_done.html')
# Create your views here.
