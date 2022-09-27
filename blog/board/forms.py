from django import forms
from .models import *
from django.forms import TextInput


class AddNoteForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=2000)
