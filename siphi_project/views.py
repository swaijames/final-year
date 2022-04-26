from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def movie(request):
    return render(request, 'movie.html')


def contact(request):
    return render(request, 'contact.html')


def movie_details(request):
    return render(request, 'movie-details.html')
# Create your views here.
