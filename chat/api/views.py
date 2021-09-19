from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .. import models
from . import serializers
from ..utils import permissions


class ConversationList(generics.ListAPIView):
    serializer_class = serializers.ConversationListSerializer

    def get_queryset(self):
        return models.Conversation.objects.get_conversation(self.request.user.id)


class MessageList(generics.RetrieveAPIView):
    serializer_class = serializers.ConversationSerializer
    queryset = models.Conversation.objects.all()
    permission_classes = IsAuthenticated, permissions.ConversationAccessPermission,
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class MessageCreate(generics.CreateAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = IsAuthenticated, permissions.SendMessagePermission
