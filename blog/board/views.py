from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *

menu = [{'title': "Главная страница", 'url_name': "main_page"},
        {'title': "Создать запись", 'url_name': "create_note"},
        {'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


class SignInView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/register.html'


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'board/register.html', {'form': form})


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


def create_note(request):
    post = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.creator = User.objects.get(pk=post.pk)
            new_note.save()
            return redirect('main_page')
    else:
        form = AddNoteForm()
    context = {
        'user_pk': post.pk,
        'menu': menu,
        'form': form,
    }
    return render(request, 'board/create_note.html', context=context)


class MyNotes(ListView):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        user = User.objects.get(pk=request.user.pk)
        return Note.objects.filter(creator=user)


def my_notes(request):
    return render(request, 'board/my_notes.html', {'menu': menu})


def draft(request):
    return HttpResponse("Черновик")


def subscriptions(request):
    return HttpResponse("Подписки")


def subscribers(request):
    return HttpResponse("Подписчики")


class SpeakerNotesView(ListView):
    model = Note
    template_name = 'board/speaker.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_queryset(self):
        user_id = self.kwargs.get("speaker_id")
        user = User.objects.get(pk=user_id)
        return Note.objects.filter(creator=user)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')
