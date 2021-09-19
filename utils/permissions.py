from rest_framework.permissions import BasePermission


class UserVerifiedPermission(BasePermission):

    message = 'You must verify your account first!'

    def has_permission(self, request, view):
        return request.user.is_verified

    def has_object_permission(self, request, view, obj):
        return request.user.is_verified
