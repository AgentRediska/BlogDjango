from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('v1/user-list/', UserListView.as_view(), name='user_list'),
    path('v1/user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('v1/follower-list/', FollowerListView.as_view(), name='follower_list'),
    path('v1/subscription/<int:pk>', FollowerDetailView.as_view(), name='unsubscribe'),
    path('v1/subscribe/<int:pk>', FollowerDetailView.as_view(), name='subscribe'),
    # path('v1/notelist/', NoteAPIView.as_view(), name='note_list'),
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^v1/auth/', include('djoser.urls.authtoken')),
]
