# Generated by Django 4.0.4 on 2022-05-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siphi_project', '0003_alter_movie_description_alter_movie_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]