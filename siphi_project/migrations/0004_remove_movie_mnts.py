# Generated by Django 4.0.4 on 2022-06-23 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siphi_project', '0003_alter_movie_mnts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='mnts',
        ),
    ]
