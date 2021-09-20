from django.urls import path

from . import views

app_name = 'accounts_api'

urlpatterns = [
    path('login-user/', views.LoginUser.as_view(), name='login_user'),
    path('refresh-token/', views.RefreshTokenAPIView.as_view(), name='refresh_token'),
    path('register/', views.RegisterUser.as_view(), name='list_create'),
    path('user-list/', views.UserList.as_view(), name='list'),

    path('retrieve-update-destroy/<str:username>/',
         views.UserRetrieveUpdateDestroy.as_view(), name='retrieve_update_destroy'),

    path('verify-account/<str:method>/', views.VerifyAccount.as_view(), name='verify_account'),
]
