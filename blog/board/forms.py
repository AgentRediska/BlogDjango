from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
from django.forms import TextInput


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        labels = {
            'title': "Тема",
            'content': "Описание"
        }
        max_lengths = {
            'title': 200,
            'content': 2000
        }
        widgets = {
            'title': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 14})
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password', 'photo'}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = {'username', 'password', 'photo'}
        labels = {'username': "Имя",
                  'password': "Пароль",
                  'photo': "Фото"}
        max_lengths = {
            'username': 150,
            'password': 128
        }