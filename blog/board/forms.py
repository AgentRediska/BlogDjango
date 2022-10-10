from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
    # photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = {'username', 'photo'}


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
