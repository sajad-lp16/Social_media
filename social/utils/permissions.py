from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from relations.models import Relation
from .. import models

User = get_user_model()


class PostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.user.is_private:
                return request.user.is_superuser or obj.user == request.user or Relation.objects.filter(
                    end_user=obj.user, start_user=request.user
                ).exists()
            return True
        return request.user.is_superuser or obj.user == request.user


class UserPostPermission(BasePermission):
    message = 'You must follow first!'

    def has_permission(self, request, view):
        user = get_object_or_404(User, username=request.data.get('username'))
        if request.method in SAFE_METHODS:
            if user.is_private:
                return request.user.is_superuser or user == request.user or Relation.objects.filter(
                    end_user=user, start_user=request.user
                ).exists()
            return True
        return request.user.is_superuser or user == request.user


class AddMediaPermission(BasePermission):
    message = 'You cant add media to others posts!'

    def has_permission(self, request, view):
        return get_object_or_404(models.Post, slug=request.data.get('slug')).user == request.user
