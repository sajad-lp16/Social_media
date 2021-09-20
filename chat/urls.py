from django.urls import path, include

app_name = 'chat'

urlpatterns = [
    path('api/', include('chat.api.urls', namespace='chat_api')),
]
