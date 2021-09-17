from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny

from . import serializers

User = get_user_model()


class UserListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,
