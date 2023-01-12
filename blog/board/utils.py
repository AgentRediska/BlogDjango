from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

menu = [{'title': "Главная страница", 'url_name': "main_page"},
        {'title': "Создать запись", 'url_name': "create_note"},
        {'title': "Мои записи", 'url_name': "my_notes"},
        {'title': "Черновик", 'url_name': "draft_notes"},
        {'title': "Все пользователи", 'url_name': "all_users"},
        {'title': "Подписки", 'url_name': "subscriptions"},
        {'title': "Подписчики", 'url_name': "subscribers"}]


class ContextDataMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user_login')

    def get_data_context_mix(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context


class ContextDataListViewMixin(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('user_login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_extra = self.get_data_context_mix()
        return {**context, **context_extra}

    def get_data_context_mix(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['right_list_search'] = self.request.GET.get('right_list_search')
        return context
