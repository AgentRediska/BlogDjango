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
    subsc = Subscriptions.objects.filter(user_id=user)
    sub_user = []
    note_dict = {}
    for sub in subsc:
        sub_user.append(User.objects.get(pk=sub.subscribers_id))
        notes = Note.objects.filter(creator=sub.subscribers_id)
        for note in notes:
            author = User.objects.get(pk=note.creator.pk)
            like = Like.objects.filter(note=note).count()
            dislike = Dislike.objects.filter(note=note).count()
            note_dict[note] = (author, like, dislike)

    context = {
        'user': user,
        'menu': menu,
        'note_dict': note_dict,
        'sub_user': sub_user,
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
