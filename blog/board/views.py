from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return render(request, '')


def main_page(request):
    return render(request, 'board/main_page.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
