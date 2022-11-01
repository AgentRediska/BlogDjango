from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    photo = models.ImageField('Фото профиля', upload_to="photos/%Y/%m/%d/", default='logo.jpg')
    username = models.CharField('Никнейм', max_length=14, unique=True, validators=[username_validator],
                                error_messages={'unique': _("Пользователь с таким именем уже существует."), }, )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username}"


class Note(models.Model):
    title = models.CharField(verbose_name="Заголовок", null=False, max_length=200,
                             validators=[MinLengthValidator(10, 'Поле должно содержать не менее 10 символов')])
    content = models.CharField(verbose_name="Описание", null=False, max_length=5000,
                               validators=[MinLengthValidator(20, 'Поле должно содержать не менее 20 символов')])
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, db_index=True)
    creator = models.ForeignKey('User', verbose_name="Автор", on_delete=models.CASCADE, related_name="note_creator")
    likes = models.ManyToManyField('User', verbose_name="Поставили лайк", related_name="liked_user")
    dislikes = models.ManyToManyField('User', verbose_name="Поставили дизлайк", related_name="disliked_user")
    is_published = models.BooleanField(verbose_name="Опубликовано", default=True)

    def __str__(self):
        return f'Тема "{self.title}", автор {self.creator}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['creation_date']


class Follower(models.Model):
    user = models.ForeignKey('User', verbose_name="Подписки",
                             on_delete=models.CASCADE, related_name='owner', db_index=True)
    subscriber = models.ForeignKey('User', verbose_name="Подписчики",
                                   on_delete=models.CASCADE, related_name='subscriber')

    def __str__(self):
        return f"{self.subscriber} подписан на {self.user}"
