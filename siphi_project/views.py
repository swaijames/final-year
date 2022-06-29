from profile import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
# from hitcount.views import HitCountDetailView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import uuid
from .forms import RateForm
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# from .forms import UserCreationForm


# from .filters import MovieFilter


def index(request):
    movies = MovieImage.objects.order_by('-uploaded')[:4]
    mwatched = MovieImage.objects.filter(movie__status="MW")[:4]
    tprate = MovieImage.objects.filter(movie__status="TR")[:4]
    Action = MovieImage.objects.filter(movie__category="A")[:4]
    Drama = MovieImage.objects.filter(movie__category="D")[:4]
    Comedy = MovieImage.objects.filter(movie__category="C")[:4]
    Horror = MovieImage.objects.filter(movie__category="H")[:4]
    hvote = MovieImage.objects.all().filter(movie__stars__gte=3)[:4]
    return render(request, 'index.html',
                  {"movies": movies, "mwatched": mwatched, "tprate": tprate, "Action": Action, "Drama": Drama,
                   "Comedy": Comedy,
                   "Horror": Horror, "hvote": hvote})


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


def profile(request):
    if request.method == "POST":
        if request.POST.get('update_user') == "user_update":

            firstname = request.POST.get('firstname')
            email = request.POST.get('email')
            lastname = request.POST.get('lastname')
            # print("first", firstname, " email ", email, " last ", lastname)
            User.objects.filter(id=request.user.id).update(first_name=firstname, email=email, last_name=lastname)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signout')
        else:
            if "old_password" in form.errors:

                messages.error(request, "Your old password was entered incorrectly")
                return redirect('profile')
            elif "The two password fields didn’t match" in form.errors:
                messages.error(request, "The two password fields didn’t match")
                return redirect('profile')
            else:
                messages.error(request, "The password is too similar to the last name")
                return redirect('profile')

    movie = Movie.objects.all()[:10]
    reviewedmovie = Movie.objects.filter(status="TR", stars__gte=3)[:10]
    form = PasswordChangeForm(request.user)

    context = {
        "movie": movie,
        "reviewedmovie": reviewedmovie,
        "form": form
    }
    return render(request, 'profile.html', context)


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
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = MovieFilter(self.request.GET, queryset=self.get_queryset())

    if 'search' in request.GET:
        search = request.GET['search']

        Drama = MovieImage.objects.filter(movie__title__icontains=search)
        Horror = MovieImage.objects.filter(movie__title__icontains=search)
        Comedy = MovieImage.objects.filter(movie__title__icontains=search)
        Action = MovieImage.objects.filter(movie__title__icontains=search)
    else:
        Drama = MovieImage.objects.filter(movie__category="D")[:4]
        Horror = MovieImage.objects.filter(movie__category="H")[:4]
        Comedy = MovieImage.objects.filter(movie__category="C")[:4]
        Action = MovieImage.objects.filter(movie__category="A")[:4]

    return render(request, 'movie.html',
                  {"Action": Action, "Drama": Drama, "Comedy": Comedy,
                   "Horror": Horror})


@login_required
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


def movie_details(request, id):
    video = MovieImage.objects.get(movie__id=id)
    print(id)
    hvote = MovieImage.objects.all().filter(movie__stars__gte=3)[:4]
    if request.method == "POST":
        form = RateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = RateForm()
    # count_hit = True
    return render(request, 'movie-details.html', {"form": form, "video": video, "hvote": hvote})


def update_rate(request, id):
    video = MovieImage.objects.get(movie__id=id)
    if request.method == "POST":
        form = RateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = RateForm()
    return render(request, 'movie-details.html', {"form": form, "video": video})


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

@login_required
def setcookie(request):
    html = HttpResponse("<h1>welcome to swahiliflx movies</h1>")
    html.set_cookie('swahiliflx', 'We are setting a cookie', max_age=None)
    return html


@login_required
def showcookie(request):
    show = request.COOKIES['swahiliflx']
    html = "<center> New Page <br>{0}</center>".format(show)
    return HttpResponse(html)
