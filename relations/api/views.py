from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from utils.permissions import UserVerifiedPermission
from . import serializers
from .. import models

User = get_user_model()


class UserFollowingsAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.RelationSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission

    def get_queryset(self):
        return models.Relation.objects.filter(start_user=self.request.user)

    def perform_create(self, serializer):
        start_user = self.request.user
        end_user = get_object_or_404(User, username=serializer.validated_data.pop('target'))
        if end_user == start_user:
            return Response({'Message': 'You cant Follow Yourself'}, status=status.HTTP_204_NO_CONTENT)
        relation = models.Relation.objects.filter(start_user=start_user, end_user=end_user)
        if relation.exists():
            relation.first().delete()
            return Response({'Message': f'User {end_user} was Unfollowed!'})
        serializer.save(start_user=start_user, end_user=end_user)


class UserFollowersListAPIView(generics.ListAPIView):
    serializer_class = serializers.RelationSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission

    def get_queryset(self):
        return models.Relation.objects.filter(end_user=self.request.user)


class UserFollowersDestroyAPIView(generics.DestroyAPIView):
    serializer_class = serializers.RelationSerializer
    permission_classes = IsAuthenticated, UserVerifiedPermission

    def get_object(self):
        return get_object_or_404(
            models.Relation, start_user__username=self.request.data.get('username'),end_user=self.request.user
        )
