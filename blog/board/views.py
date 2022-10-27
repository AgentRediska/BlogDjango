from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
import re

from .forms import *
from .models import *

menu = [{'title': "Главная страница", 'url_name': "main_page"},
        {'title': "Создать запись", 'url_name': "create_note"},
        {'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft_notes"},
        {'title': "Все пользователи", 'url_name': "all_users"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


class SignInView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/register.html'


class UserEditView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('main_page')
    template_name = 'board/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    template_name = 'board/change_password.html'
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'board/register.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, {'form': form})


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
        context['right_list_search'] = self.request.GET.get('right_list_search')
        context['menu'] = menu
        return context

    def get_queryset(self):
        request = self.request
        subsc = Subscription.objects.filter(user_id=request.user.pk)
        notes = []
        for sub in subsc:
            notes.extend(list(Note.objects.filter(creator=sub.subscription_id, is_published=True)))
        notes.sort(key=lambda x: x.creation_date)
        return notes


class CreateNoteView(CreateView):
    form_class = AddNoteForm
    template_name = 'board/create_note.html'
    success_url = reverse_lazy("my_notes")
    pk_url_kwarg = 'note_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateNoteView, self).form_valid(form)


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
        return Note.objects.filter(creator=user, is_published=True)


class DraftNotesView(ListView):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 2

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(DraftNotesView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def get_queryset(self):
        request = self.request
        user = User.objects.get(pk=request.user.pk)
        return Note.objects.filter(creator=user, is_published=False)


class EditNoteView(UpdateView):
    model = Note
    form_class = AddNoteForm
    template_name = 'board/create_note.html'
    success_url = reverse_lazy("my_notes")
    pk_url_kwarg = 'note_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        context['title'] = 'Редактировать запись'
        return context


class DetailNoteView(DetailView):
    model = Note
    template_name = 'board/detail_note.html'
    pk_url_kwarg = 'note_pk'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context


class SubscriptionsView(ListView):
    model = User
    template_name = 'board/center_subscr/my_subscriptions.html'
    context_object_name = 'subscr_list'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(SubscriptionsView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def get_queryset(self):
        request = self.request
        subscriptions = Subscription.objects.filter(user=request.user)
        sub_user = []
        search_text = ""
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
        for sub in subscriptions:
            user = User.objects.get(pk=sub.subscription_id)
            if re.search(search_text, user.username, re.IGNORECASE):
                sub_user.append(user)
        return sub_user


class SubscribersView(ListView):
    model = User
    template_name = 'board/center_subscr/my_subscribers.html'
    context_object_name = 'subscr_list'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(SubscribersView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def get_queryset(self):
        request = self.request
        subscribers = Subscription.objects.filter(subscription_id=request.user.pk)
        sub_user = []
        search_text = ""
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
        for sub in subscribers:
            user = User.objects.get(pk=sub.user.pk)
            if re.search(search_text, user.username, re.IGNORECASE):
                sub_user.append(user)
        sub_user.sort(key=lambda us: us.username)
        return sub_user


class AllUsersView(ListView):
    model = User
    template_name = 'board/center_subscr/all_users.html'
    context_object_name = 'subscr_list'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_login')
        return super(AllUsersView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context

    def get_queryset(self):
        request = self.request
        search_text = ""
        if self.request.GET.get("center_list_search"):
            search_text = self.request.GET.get("center_list_search")
        users = User.objects.filter(~Q(pk=request.user.pk), username__icontains=search_text).order_by('username')
        return users


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
        speaker_id = self.kwargs.get("speaker_id")
        user_speaker = User.objects.get(pk=speaker_id)
        is_subscription = Subscription.objects.filter(subscription_id=self.request.user.id, user=user_speaker)
        is_subscribe = Subscription.objects.filter(subscription_id=speaker_id, user=self.request.user)
        context['menu'] = menu
        context["speaker"] = user_speaker
        context['is_subscribe'] = is_subscribe
        context['is_subscription'] = is_subscription
        return context

    def get_queryset(self):
        user_id = self.kwargs.get("speaker_id")
        user = User.objects.get(pk=user_id)
        return Note.objects.filter(creator=user, is_published=True)


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


def unfollow_user(request, sub_pk):
    Subscription.objects.filter(subscription_id=sub_pk, user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe_user(request, sub_pk):
    user = User.objects.get(pk=sub_pk)
    Subscription.objects.filter(subscription_id=request.user.pk, user=user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribe_to_user(request, sub_pk):
    subscription = Subscription()
    subscription.subscription_id = sub_pk
    subscription.user = request.user
    subscription.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
