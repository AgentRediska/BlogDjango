from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='login'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    # path('my_page/<slug:user_slug>/', main_page),
    path('create_note/<slug:user_slug>/', create_note, name='create_note'),
    path('my_notes/', my_notes, name='my_notes'),
    path('draft/', draft, name='draft'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('subscribers/', subscribers, name='subscribers'),
]
