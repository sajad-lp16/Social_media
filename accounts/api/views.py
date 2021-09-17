from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny

from . import serializers
from ..utils.permissions import AccountOwnerPermission

User = get_user_model()


class UserListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    permission_classes = AccountOwnerPermission,
