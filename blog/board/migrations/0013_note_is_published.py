# Generated by Django 4.1.1 on 2022-10-23 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_rename_user_id_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
