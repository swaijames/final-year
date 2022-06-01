from uuid import uuid4
import datetime

from django.db import models
from django.db.models.aggregates import Sum
from django.conf import settings

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

    def __str__(self):
        return '{} ({})'.format(self.title, self.year_of_release)


#
# class MovieImage(models.Model):
#     image = models.ImageField(upload_to='Movie')
#     uploaded = models.DateTimeField(auto_now_add=True)
#     movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.movie)
