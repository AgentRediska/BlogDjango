from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *

"""{'title': "Создать запись", 'url_name': "create_note/<slug:user_slug>/"}"""
menu = [{'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


class SignInView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/index.html'


class UserLoginView(LoginView):
    template_name = 'board/login.html'


class UserLogoutView(LogoutView):
    next_page = "/"


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {'menu': menu, }
            return render(request, 'board/main_page.html', context)
        else:
            response = redirect('board/login/')
            return response


def index(request):
    return render(request, 'board/index.html')


def main_page(request):
    user_pk = request.user.pk
    get_object_or_404(User, pk=user_pk)
    context = {
        'user_pk': user_pk,
        'menu': menu,
    }
    return render(request, 'board/main_page.html', context=context)


def create_note(request, user_slug):
    post = get_object_or_404(User, slug=user_slug)
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.creator = User.objects.get(pk=post.pk)
            new_note.save()
            return redirect('login')
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
