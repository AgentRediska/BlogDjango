from django.urls import path

from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register', UserRegistrationView.as_view(), name='user_register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(), name='password'),
    path('create_note/', CreateNoteView.as_view(), name='create_note'),
    path('edit_note/<int:note_pk>/', EditNoteView.as_view(), name='edit_note'),
    path('delete_note/<int:note_pk>/', delete_note, name="delete_note"),
    path('detail_note/<int:note_pk>/', DetailNoteView.as_view(), name='detail_note'),
    path('my_notes/', MyNotesView.as_view(), name='my_notes'),
    path('set_like/<int:note_pk>/', like_post, name='set_like'),
    path('set_dislike/<int:note_pk>/', dislike_post, name='set_dislike'),
    path('draft/', DraftNotesView.as_view(), name='draft_notes'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('unfollow_user/<int:sub_pk>/', unfollow_user, name='unfollow_user'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers'),
    path('unsubscribe_from_user/<int:sub_pk>/', unsubscribe_from_user, name='unsubscribe_from_user'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('speaker/<int:speaker_id>/', SpeakerNotesView.as_view(), name='speaker'),
    path('subscribe_to_user/<int:sub_pk>/', subscribe_to_user, name='subscribe_to_user')
]
