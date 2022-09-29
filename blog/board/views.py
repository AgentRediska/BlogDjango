from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *

"""{'title': "Создать запись", 'url_name': "create_note/<slug:user_slug>/"}"""
menu = [{'title': "Мои записи", 'url_name': "my_notes"},
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
    }
    return render(request, 'board/main_page.html', context=context)


def create_note(request, user_slug):
    post = get_object_or_404(User, slug=user_slug)
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            try:
                Note.objects.create(**form.cleaned_data)
                return redirect('create_note')
            except (Exception,):
                form.add_error(None, 'Ошибка добавления записи')
    else:
        form = AddNoteForm()
    context = {
        'user_pk': post.pk,
        'menu': menu,
        'form': form,
    }
    return render(request, 'board/create_note.html', context=context)


def my_notes(request):
    return render(request, 'board/my_notes.html', {'menu': menu})


def draft(request):
    return HttpResponse("Черновик")


def subscriptions(request):
    return HttpResponse("Подписки")


def subscribers(request):
    return HttpResponse("Подписчики")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
