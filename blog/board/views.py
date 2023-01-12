from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms import *
from .models import *
from .utils import *
from services.follower import *
from services.note import *
from services.user import *


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


class MainPageView(ContextDataListViewMixin):
    model = Note
    template_name = 'board/main_page.html'
    context_object_name = 'notes'
    paginate_by = 30

    def get_queryset(self):
        return get_subscription_notes(get_subscriptions(self.request.user))


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


class MyNotesView(ContextDataListViewMixin):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        return get_user_notes(self.request.user)


class DraftNotesView(ContextDataListViewMixin):
    model = Note
    template_name = 'board/my_notes.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        return get_user_draft_notes(self.request.user)


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


class SubscriptionsView(ContextDataListViewMixin):
    model = User
    template_name = 'board/center_subscr/my_subscriptions.html'
    context_object_name = 'subscr_list'
    paginate_by = 16

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            subscriptions = get_subscriptions(self.request.user, self.request.GET.get("center_list_search"))
        else:
            subscriptions = get_subscriptions(self.request.user)
        return get_users_by_follower(subscriptions)


class SubscribersView(ContextDataListViewMixin):
    model = User
    template_name = 'board/center_subscr/my_subscribers.html'
    context_object_name = 'subscr_list'
    paginate_by = 16

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            subscribers = get_subscribers(self.request.user, self.request.GET.get("center_list_search"))
        else:
            subscribers = get_subscribers(self.request.user)
        return get_users_by_follower(subscribers)


class AllUsersView(ContextDataListViewMixin):
    model = User
    template_name = 'board/center_subscr/all_users.html'
    context_object_name = 'subscr_list'
    paginate_by = 40

    def get_queryset(self):
        if self.request.GET.get("center_list_search"):
            return get_users(self.request.user, self.request.GET.get("center_list_search"))
        else:
            return get_users(self.request.user)


class SpeakerNotesView(ContextDataListViewMixin):
    model = Note
    template_name = 'board/speaker.html'
    context_object_name = 'notes'
    paginate_by = 16

    def get_context_data(self, *, object_list=None, **kwargs):
        user_speaker = User.objects.get(pk=self.kwargs.get("speaker_id"))
        rel = check_user_relationship(self.request.user, user_speaker)
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix(
            speaker=user_speaker,
            is_subscribe=rel[0],
            is_subscription=rel[1])
        return {**context, **context_extra}

    def get_queryset(self):
        return get_user_notes(self.kwargs.get("speaker_id"))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found<h1>')


def like_post(request, note_pk):
    set_like_to_note(request.user, note_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislike_post(request, note_pk):
    set_dislike_to_note(request.user, note_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_note(request, note_pk):
    Note.objects.get(pk=note_pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_user(request, sub_pk):
    exclude_user_from_subscriptions(request.user, sub_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe_from_user(request, sub_pk):
    unsubscribe(request.user, sub_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribe_to_user(request, sub_pk):
    subscribe(request.user, sub_pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
