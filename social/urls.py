from django.urls import path, include

app_name = 'social'

urlpatterns = [
    path('api/', include('social.api.urls')),
]
