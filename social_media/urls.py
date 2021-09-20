from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('activity/', include('activity.urls', namespace='activity')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('relations/', include('relations.urls', namespace='relations')),
    path('social/', include('social.urls', namespace='social')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
