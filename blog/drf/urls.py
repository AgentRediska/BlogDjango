from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('v1/user-list/', UserListView.as_view(), name='user_list'),
    path('v1/user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    # path('v1/notelist/', NoteAPIView.as_view(), name='note_list'),
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^v1/auth/', include('djoser.urls.authtoken')),
]
