from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('movie', views.movie, name='movie'),
    path('contact', views.contact, name='contact'),
    path('movie_detail', views.movie_details, name='movie_detail'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]
