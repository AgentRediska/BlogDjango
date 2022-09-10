from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return HttpResponse("Страница приложения c входом")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
