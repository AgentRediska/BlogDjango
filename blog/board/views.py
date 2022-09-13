from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *

menu = [{'title': "Создать запись", 'url_name': "create_note"},
        {'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


def index(request):
    return render(request, 'board/index.html')


def main_page(request):
    user = User.objects.get(pk=1)
    return render(request, 'board/main_page.html', {'user': user})


def create_note(request):
    return HttpResponse("Создать запись")


def my_notes(request):
    return HttpResponse("Мои записи")


def draft(request):
    return HttpResponse("Черновик")


def subscriptions(request):
    return HttpResponse("Подписки")


def subscribers(request):
    return HttpResponse("Подписчики")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
