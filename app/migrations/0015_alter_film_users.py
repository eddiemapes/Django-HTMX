# Generated by Django 5.0.7 on 2024-08-16 14:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_film_options_userfilms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='users',
        ),
        migrations.AddField(
            model_name='film',
            name='users',
            field=models.ManyToManyField(related_name='films', through='app.UserFilms', to=settings.AUTH_USER_MODEL),
        ),
            

    ]
