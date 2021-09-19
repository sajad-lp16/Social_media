from rest_framework.permissions import BasePermission


class ConversationAccessPermission(BasePermission):

    message = 'You cant see others conversations!'

    def has_object_permission(self, request, view, obj):
        return obj.start_user == request.user or request.user.is_superuser or obj.end_user == request.user


class SendMessagePermission(BasePermission):

    message = 'You can only send message to flowers and followings!'

    def has_object_permission(self, request, view, obj):
        target = obj.get_contact_user
        return target in obj.user.followers or target in obj.user.followings


class MessageOwnerPermission(BasePermission):

    message = 'You cant modify your messages only!'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
