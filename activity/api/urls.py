from django.urls import path

from . import views

app_name = 'activity_api'

urlpatterns = [
    path('post-comments/', views.CommentPostListCreate.as_view(), name='post_comments'),
    path('comment-likes/', views.CommentLikeListCreate.as_view(), name='comment_likes'),
    path('post-likes/', views.PostLikesListCreate.as_view(), name='post_likes'),
    path('message-likes/', views.MessageLikeListCreate.as_view(), name='message_likes'),
]
