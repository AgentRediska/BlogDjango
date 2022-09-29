from django import forms
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
