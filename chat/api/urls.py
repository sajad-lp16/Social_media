from django.urls import path

from . import views

app_name = 'chat_api'

urlpatterns = [
    path('send-message/', views.MessageCreate.as_view(), name='send_message'),
    path('edit-message/', views.MessageRetrieveUpdateDestroy.as_view(), name='edit_message'),
    path('message-list/<str:slug>/', views.MessageList.as_view(), name='message_list'),
    path('conversation-list/', views.ConversationList.as_view(), name='conversation_list'),
]
