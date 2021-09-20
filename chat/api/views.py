from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from utils.permissions import UserVerifiedPermission
from .. import models
from . import serializers
from ..utils import permissions


class ConversationList(generics.ListAPIView):
    serializer_class = serializers.ConversationListSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission

    def get_queryset(self):
        return models.Conversation.objects.get_conversation(self.request.user.id)


class MessageList(generics.RetrieveAPIView):
    serializer_class = serializers.ConversationSerializer
    queryset = models.Conversation.objects.all()
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.ConversationAccessPermission
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class MessageCreate(generics.CreateAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.SendMessagePermission


class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.MessageOwnerPermission

    def get_object(self):
        instance = get_object_or_404(models.Message, id=self.request.data.get('id'))
        self.check_object_permissions(self.request, instance)
        return instance
