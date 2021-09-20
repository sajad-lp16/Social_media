from django.urls import path, include

app_name = 'relations'

urlpatterns = [
    path('api/', include('relations.api.urls', namespace='relation_api'))
]
