from django.urls import path

from . import views

app_name = 'relations_api'

urlpatterns = [
    path('followings/', views.UserFollowingsAPIView.as_view(), name='user_followings'),
    path('followers/', views.UserFollowersListAPIView.as_view(), name='user_followers'),
    path('delete-follower/', views.UserFollowersDestroyAPIView.as_view(), name='delete_follower'),
]
