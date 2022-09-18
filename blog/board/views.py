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
    user = User.objects.get(pk=2)
    # subscribers = Subscribers.objects.filter(user_id=user.pk)
    # notes = {}
    # for sub in subscribers:
    #     note = Note.objects.get(creator_id=sub)
    #     note_author = User.objects.get(pk=note.creator)
    #     notes.add(note: note_author)

    notes = Note.objects.filter(creator_id=1)
    note_author = User.objects.get(pk=1)
    contex = {
        'user': user,
        'menu': menu,
        'notes': notes,
        'note_author': note_author,
        'title': 'Главная страница'
    }
    return render(request, 'board/main_page.html', context=contex)


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
