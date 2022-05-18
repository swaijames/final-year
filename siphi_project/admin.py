from django.contrib import admin
from .models import Movie, MovieImage, Vote, Profile

admin.site.register(Movie)
admin.site.register(MovieImage)
admin.site.register(Vote)
admin.site.register(Profile)
