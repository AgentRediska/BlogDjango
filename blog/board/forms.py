from django import forms
from .models import *
from django.forms import TextInput


class AddNoteForm(forms.Form):
    title = forms.CharField(max_length=200, label="Тема",
                            widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}))
    content = forms.CharField(max_length=2000, label="Описание",
                              widget=forms.Textarea(attrs={'cols': 80, 'rows': 14}))
