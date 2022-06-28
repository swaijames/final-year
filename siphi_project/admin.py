from django.contrib import admin
from .models import Movie, MovieImage, Vote, Profile, Genre, MovieGenre

admin.site.register(Movie)
admin.site.register(MovieImage)
admin.site.register(Vote)
admin.site.register(Profile)
# admin.site.register(Genre)
# admin.site.register(MovieGenre)
