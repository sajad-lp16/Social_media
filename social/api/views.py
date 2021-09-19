from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .. import models
from ..utils import permissions
from utils.permissions import UserVerifiedPermission


class FollowingPostsList(generics.ListAPIView):
    permission_classes = IsAuthenticated, UserVerifiedPermission
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        self.check_permissions(self.request)
        return models.Post.objects.get_followings_posts(self.request.user)


class UserPostsList(generics.ListAPIView):
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.UserPostPermission
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        self.check_permissions(self.request)
        return models.Post.objects.get_user_posts(self.kwargs.get('username'))


class MyPostsListCreate(generics.ListCreateAPIView):
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.PostPermission
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        self.check_permissions(self.request)
        return models.Post.objects.get_user_posts(self.request.user.username)


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.PostPermission
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()

    def get_object(self):
        instance = get_object_or_404(models.Post, slug=self.request.data.get('slug'))
        self.check_object_permissions(self.request, instance)
        return instance


class MediaCreate(generics.CreateAPIView):
    permission_classes = IsAuthenticated, UserVerifiedPermission, permissions.AddMediaPermission
    serializer_class = serializers.MediaSerializer
    queryset = models.Media.objects.all()
