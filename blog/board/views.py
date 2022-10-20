from functools import reduce
from operator import and_

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
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


class MainPageView(ListView):
    model = Note
    template_name = 'board/main_page.html'
    context_object_name = 'notes'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(MainPageView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_queryset(self):
        request = self.request
        subsc = Subscription.objects.filter(user_id=request.user.pk)
        notes = []
        for sub in subsc:
            notes.extend(list(Note.objects.filter(creator=sub.subscription_id)))
        notes.sort(key=lambda x: x.creation_date)
        return notes


def index(request):
    return render(request, 'board/index.html')


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


class MyNotesView(ListView):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 2

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(MyNotesView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def get_queryset(self):
        request = self.request
        user = User.objects.get(pk=request.user.pk)
        return Note.objects.filter(creator=user)


def draft(request):
    return HttpResponse("Черновик")


def subscriptions(request):
    return HttpResponse("Подписки")


class SubscriptionsView(ListView):
    model = User
    template_name = 'board/my_subscriptions.html'
    context_object_name = 'subscriptions'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(SubscriptionsView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        user = User.objects.get(pk=request.user.pk)
        return Note.objects.filter(creator=user)

def subscribers(request):
    return HttpResponse("Подписчики")


class SpeakerNotesView(ListView):
    model = Note
    template_name = 'board/speaker.html'
    context_object_name = 'notes'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(SpeakerNotesView, self).get(*args, **kwargs)

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


def like_post(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    if request.user in note.likes.all():
        print("YEEEEEEEEEES")
    else:
        print("NOOOOOOO")
    if note.likes.filter(id=request.user.pk).exists():
        note.likes.remove(request.user)
    else:
        if note.dislikes.filter(id=request.user.pk).exists():
            note.dislikes.remove(request.user)
        note.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislike_post(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    if note.dislikes.filter(id=request.user.pk).exists():
        note.dislikes.remove(request.user)
    else:
        if note.likes.filter(id=request.user.pk).exists():
            note.likes.remove(request.user)
        note.dislikes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
