# Generated by Django 4.1.1 on 2022-09-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_rename_subscribers_subscriptions_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='Subscription',
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['creation_date'], 'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['name'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='subscriptions_id',
            new_name='subscription_id',
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(default=222, max_length=30, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
