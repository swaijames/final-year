# Generated by Django 4.0.4 on 2022-05-11 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import siphi_project.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('plot', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('rating', models.IntegerField(choices=[(0, 'NR - Not Rate'), (1, 'G - General Audiences'),
                                                        (2, 'PG – Parental Guidance Suggested'),
                                                        (3, 'PG-13 – Parents Strongly Cautioned'),
                                                        (4, 'R – Restricted'), (5, 'NC-17 – Adults Only')], default=0)),
                ('runtime', models.PositiveIntegerField()),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('-year', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=140)),
                ('last_name', models.CharField(max_length=140)),
                ('born', models.DateField()),
                ('died', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='siphi_project.movie')),
                (
                'person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='siphi_project.person')),
            ],
            options={
                'unique_together': {('movie', 'person', 'name')},
            },
        ),

        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='acting_credits', through='siphi_project.Role',
                                         to='siphi_project.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='directed', to='siphi_project.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='writing_credits', to='siphi_project.person'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(choices=[(1, '👍'), (-1, '👎')])),
                ('voted_on', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siphi_project.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'movie')},
            },
        ),
    ]