from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    path('v1/userlist/', UserAPIView.as_view(), name='user_list'),
    path('v1/notelist/', NoteAPIView.as_view(), name='note_list'),
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^v1/auth/', include('djoser.urls.authtoken')),
]
