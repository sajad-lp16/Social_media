from django.db.models import Q

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from relations.models import Relation
from .. import models


class ConversationAccessPermission(BasePermission):
    message = 'You cant see others conversations!'

    def has_object_permission(self, request, view, obj):
        return obj.start_user == request.user or request.user.is_superuser or obj.end_user == request.user


class SendMessagePermission(BasePermission):
    message = 'You can only send message to flowers and followings!'

    def has_permission(self, request, view):
        conversation = get_object_or_404(models.Conversation, slug=request.data.get('conversation_slug'))
        user = conversation.start_user
        if request.user == conversation.start_user:
            user = conversation.end_user
        return Relation.objects.filter(
            Q(start_user=request.user, end_user=user) |
            Q(start_user=user, end_user=request.user)
        ).exists()


class MessageOwnerPermission(BasePermission):
    message = 'You cant modify your messages only!'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
