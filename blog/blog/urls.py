from django.contrib import admin
from django.urls import path, include

from board.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
]


handler404 = page_not_found
