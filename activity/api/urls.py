from django.urls import path

from . import views

app_name = 'activity_api'

urlpatterns = [
    path('post-comments/', views.CommentPostListCreate.as_view(), name='post_comments'),
]
