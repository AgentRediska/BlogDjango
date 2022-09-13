from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *


def index(request):
    return render(request, '')


def main_page(request):
    user = User.objects.get(pk=1)
    return render(request, 'board/main_page.html', {'user': user})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
