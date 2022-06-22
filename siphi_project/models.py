from uuid import uuid4
import uuid
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Sum
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return '{}'.format(self.user)


NOT_RATED = 0
RATED_G = 1
RATED_PG = 2
RATED_PG13 = 3
RATED_R = 4
RATED_NC17 = 5
RATINGS = (
    (NOT_RATED, 'NR - Not Rate'),
    (RATED_G, 'G - General Audiences'),
    (RATED_PG, 'PG – Parental Guidance Suggested'),
    (RATED_PG13, 'PG-13 – Parents Strongly Cautioned'),
    (RATED_R, 'R – Restricted'),
    (RATED_NC17, 'NC-17 – Adults Only'),
)

CATEGORY_CHOICES = (
    ('C', 'Comedy'),
    ('A', 'Action'),
    ('D', 'Drama'),
    ('H', 'Horror'),
)

STATUS_CHOICES = (
    ('RA', 'recently-added'),
    ('MW', 'most-watched'),
    ('TR', 'top-rated'),
)


class Movie(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(max_length=5000, blank=False, null=False)
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED, blank=False, null=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1, null=True, blank=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, null=True, blank=False)
    year_of_release = models.DateField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    url = models.URLField(null=False, blank=False, default="https://youtu.be/0Lg7AsrgBAY")

    def __str__(self):
        return '{} ({})'.format(self.title, self.year_of_release)


#
class MovieImage(models.Model):
    image = models.ImageField(upload_to='Movie')
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.movie)


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "👍"),
        (DOWN, "👎")
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}({})'.format(self.movie, self.value)


class Meta:
    unique_together = ('user', 'movie')


class Genre(models.Model):
    genre_name = models.CharField(choices=CATEGORY_CHOICES, null=False, blank=False, max_length=150)

    def category_id(self):
        return self.id

    def __str__(self):
        return '{}'.format(self.genre_name)


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return '{}({})'.format(self.id, self.movie)
