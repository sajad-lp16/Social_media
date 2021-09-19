from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
