from django import forms
from .models import *


class AddNoteForm(forms.Form):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
