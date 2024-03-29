# Generated by Django 4.1.1 on 2022-10-17 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_remove_like_note_remove_like_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='dislikes',
            field=models.ManyToManyField(related_name='disliked_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='note',
            name='likes',
            field=models.ManyToManyField(related_name='liked_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
