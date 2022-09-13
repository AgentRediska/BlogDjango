from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='login'),
    path('my_page/', main_page),
    path('create_note/', create_note, name='create_note'),
    path('my_notes/', my_notes, name='my_notes'),
    path('draft/', draft, name='draft'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('subscribers/', subscribers, name='subscribers'),
]
