from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


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
        fields = {'username', 'photo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Пароль не должен быть слишком похож на другую вашу личную информацию.\n' \
                                             'Ваш пароль должен содержать как минимум 8 символов.\n' \
                                             'Пароль не должен быть слишком простым и распространенным.\n' \
                                             'Пароль не может состоять только из цифр.'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
