from django.urls import path, include

app_name = 'activity'

urlpatterns = [
    path('api/', include('activity.api.urls', namespace='activity_api')),
]
