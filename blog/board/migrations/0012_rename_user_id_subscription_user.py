# Generated by Django 4.1.1 on 2022-10-20 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_note_dislikes_note_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='user_id',
            new_name='user',
        ),
    ]
