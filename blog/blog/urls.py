from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog import settings
from board.views import page_not_found, MainPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', MainPageView.as_view(), name='main_page'),
    path('board/', include('board.urls')),
    path('api/', include('drf.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
