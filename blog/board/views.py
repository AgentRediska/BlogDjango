from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from .models import *

menu = [{'title': "Создать запись", 'url_name': "create_note"},
        {'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


def index(request):
    return render(request, 'board/index.html')


def main_page(request, user_slug):
    post = get_object_or_404(User, slug=user_slug)
    context = {
        'user_pk': post.pk,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'board/main_page.html', context=context)


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
