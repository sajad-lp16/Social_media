from django.urls import path

from . import views

app_name = 'social_api'

urlpatterns = [
    path('my-posts-list-create/', views.MyPostsListCreate.as_view(), name='my_posts'),
    path('user-posts/<str:username>/', views.UserPostsList.as_view(), name='user_posts'),
    path('followings-posts/', views.FollowingPostsList.as_view(), name='post_list_create'),
    path('get-edit-posts/', views.PostRetrieveUpdateDestroy.as_view(), name='get_edit_posts'),
    path('add-media/', views.MediaCreate.as_view(), name='add_media'),
]
