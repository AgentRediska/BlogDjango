from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
import re

from .forms import *
from .models import *
from .utils import *


class SignInView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/register.html'


class UserEditView(ContextDataMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}

    def get_object(self, queryset=None):
        return self.request.user


class PasswordsChangeView(ContextDataMixin, PasswordChangeView):
    template_name = 'board/change_password.html'
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}


class UserRegistrationView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'board/register.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, 'board/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'board/login.html'


class UserLogoutView(LogoutView):
    next_page = "/"


class MainPageView(ContextDataMixin, ListView):
    model = Note
    template_name = 'board/main_page.html'
    context_object_name = 'notes'
    paginate_by = 30

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}

    def get_queryset(self):
        subscriptions = Follower.objects.filter(subscriber=self.request.user).values('user')
        notes = Note.objects.filter(creator__in=subscriptions, is_published=True).order_by('creation_date')
        return notes


class CreateNoteView(ContextDataMixin, CreateView):
    form_class = AddNoteForm
    template_name = 'board/create_note.html'
    success_url = reverse_lazy("my_notes")
    pk_url_kwarg = 'note_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(title='Создать запись')
        return {**context, **context_extra}

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateNoteView, self).form_valid(form)


class MyNotesView(ContextDataMixin, ListView):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}

    def get_queryset(self):
        return Note.objects.filter(creator=self.request.user, is_published=True)


class DraftNotesView(ContextDataMixin, ListView):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}

    def get_queryset(self):
        return Note.objects.filter(creator=self.request.user, is_published=False)


class EditNoteView(ContextDataMixin, UpdateView):
    model = Note
    form_class = AddNoteForm
    template_name = 'board/create_note.html'
    success_url = reverse_lazy("my_notes")
    pk_url_kwarg = 'note_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(title='Редактировать запись')
        return {**context, **context_extra}


class DetailNoteView(ContextDataMixin, DetailView):
    model = Note
    template_name = 'board/detail_note.html'
    pk_url_kwarg = 'note_pk'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}


class SubscriptionsView(ContextDataMixin, ListView):
    model = User
    template_name = 'board/center_subscr/my_subscriptions.html'
    context_object_name = 'subscr_list'
    paginate_by = 16

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(title='Создать запись')
        return {**context, **context_extra}

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
            subscriptions = Follower.objects.filter(subscriber=self.request.user,
                                                    user__username__icontains=search_text).values('user')
        else:
            subscriptions = Follower.objects.filter(subscriber=self.request.user).values('user')
        sub_user = User.objects.filter(pk__in=subscriptions)\
            .only('pk', 'username', 'photo', 'date_joined').order_by('username')
        return sub_user


class SubscribersView(ContextDataMixin, ListView):
    model = User
    template_name = 'board/center_subscr/my_subscribers.html'
    context_object_name = 'subscr_list'
    paginate_by = 16

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(title='Создать запись')
        return {**context, **context_extra}

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
            subscribers = Follower.objects.filter(user=self.request.user,
                                                  subscriber__username__icontains=search_text).values('subscriber')
        else:
            subscribers = Follower.objects.filter(user=self.request.user).values('subscriber')
        sub_user = User.objects.filter(pk__in=subscribers)\
            .only('pk', 'username', 'photo', 'date_joined').order_by('username')
        return sub_user


class AllUsersView(ContextDataMixin, ListView):
    model = User
    template_name = 'board/center_subscr/all_users.html'
    context_object_name = 'subscr_list'
    paginate_by = 40

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(title='Создать запись')
        return {**context, **context_extra}

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
            users = User.objects.filter(~Q(pk=self.request.user.pk),username__icontains=search_text)\
                .only('pk', 'username', 'photo', 'date_joined').order_by('username')
        else:
            users = User.objects.filter(~Q(pk=self.request.user.pk))\
                .only('pk', 'username', 'photo', 'date_joined').order_by('username')
        return users


class SpeakerNotesView(ContextDataMixin, ListView):
    model = Note
    template_name = 'board/speaker.html'
    context_object_name = 'notes'
    paginate_by = 16

    def get_context_data(self, *, object_list=None, **kwargs):
        user_speaker = User.objects.get(pk=self.kwargs.get("speaker_id"))
        is_subscription = Follower.objects.filter(user=self.request.user, subscriber=user_speaker)
        is_subscribe = Follower.objects.filter(user=user_speaker, subscriber=self.request.user)
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(speaker=user_speaker, is_subscribe=is_subscribe,
                                                  is_subscription=is_subscription)
        return {**context, **context_extra}

    def get_queryset(self):
        return Note.objects.filter(creator=self.kwargs.get("speaker_id"), is_published=True)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')


def like_post(request, note_pk):
    note = Note.objects.get(pk=note_pk)
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


def delete_note(request, note_pk):
    Note.objects.get(pk=note_pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_user(request, sub_pk):
    """Исключить пользователя из списка ваших подписчиков"""
    print("unfollow")
    Follower.objects.filter(subscriber=User.objects.get(pk=sub_pk), user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe_from_user(request, sub_pk):
    """Отписаться от пользователя"""
    print("unsubscribe")
    print(sub_pk)
    Follower.objects.filter(subscriber=request.user, user=User.objects.get(pk=sub_pk)).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribe_to_user(request, sub_pk):
    """Подписаться на пользователя"""
    print("subscribe")
    Follower.objects.create(user=User.objects.get(pk=sub_pk), subscriber=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
