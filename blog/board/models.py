from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    photo = models.ImageField('Фото профиля', upload_to="photos/%Y/%m/%d/")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Note(models.Model):
    title = models.CharField(null=False, max_length=200)
    content = models.CharField(null=False, max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True, db_index=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="note_creator")
    liked_user = models.ManyToManyField('User', through="Like", related_name="liked_user")
    disliked_user = models.ManyToManyField('User', through="Dislike", related_name="disliked_user")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['creation_date']


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)

    def __str__(self):
        return f"user_pk: {self.user}, note_pk: {self.note}"


class Dislike(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)

    def __str__(self):
        return f"user_pk: {self.user}, note_pk: {self.note}"


class Subscription(models.Model):
    subscription_id = models.IntegerField(null=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return f"user id: {self.user_id}, subs id: {self.subscription_id}"
