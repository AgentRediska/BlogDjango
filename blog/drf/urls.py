from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('v1/users/', UserListView.as_view(), name='users'),
    path('v1/user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('v1/followers/', FollowerListView.as_view(), name='follower_list'),
    path('v1/subscription/<int:pk>', FollowerDetailView.as_view(), name='subscriptions'),
    path('v1/subscription-notes/', SubscriptionNoteListView.as_view(), name='sub_notes'),
    path('v1/user-notes/', UserNoteListView.as_view(), name='user_notes'),
    path('v1/note-detail/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('v1/note-like/<int:pk>', NoteLikeView.as_view(), name='note_like'),
    path('v1/note-dislike/<int:pk>', NoteDislikeView.as_view(), name='note_dislike'),
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^v1/auth/', include('djoser.urls.authtoken')),
]
