from django.urls import path

from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register', register_view, name='user_register'),
    path('create_note', create_note, name='create_note'),
    path('my_notes/', MyNotesView.as_view(), name='my_notes'),
    path('set_like/<int:note_pk>/', like_post, name='set_like'),
    path('set_dislike/<int:note_pk>/', dislike_post, name='set_dislike'),
    path('draft/', draft, name='draft'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('subscribers/', subscribers, name='subscribers'),
    path('speaker/<int:speaker_id>/', SpeakerNotesView.as_view(), name='speaker')
]
