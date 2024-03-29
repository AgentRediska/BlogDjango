# Generated by Django 4.1.1 on 2022-09-17 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1111, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=15),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=2000)),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_creator', to='board.user')),
                ('disliked_user', models.ManyToManyField(related_name='disliked_user', through='board.Dislike', to='board.user')),
                ('liked_user', models.ManyToManyField(related_name='liked_user', through='board.Like', to='board.user')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.note'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.user'),
        ),
        migrations.AddField(
            model_name='dislike',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.note'),
        ),
        migrations.AddField(
            model_name='dislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.user'),
        ),
    ]
