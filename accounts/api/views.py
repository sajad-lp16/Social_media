from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from ..utils.permissions import AccountOwnerPermission
from ..utils.verification_backend import generate_code
from ..utils.verification_backend import send_verification_email
from ..utils.verification_backend import send_verification_sms

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


class VerifyAccount(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        method = kwargs.get('method')
        code = generate_code()
        key_code = f'{request.user.username}'
        if method == 'sms':
            send_verification_sms.delay(code)
            cache.set(key_code, code, timeout=90)
            return Response({'message': 'Activation Code Was Sent To Your Phone'}, status=status.HTTP_200_OK)
        send_verification_email.delay(request.user.email, code)
        cache.set(key_code, code, timeout=90)
        return Response({'message': 'Activation Code Was Sent To Your Email'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        submit_code = request.data.get('code')
        auth_code = cache.get(f'{user.username}')
        if auth_code is None:
            return Response({'message': 'The Code Is Invalid Or Expired'}, status=status.HTTP_404_NOT_FOUND)
        if auth_code != submit_code:
            return Response({'message': 'The Code Is Invalid !'}, status=status.HTTP_403_FORBIDDEN)
        user.is_verified = True
        user.save()
        return Response({'message': 'The Account Has Been Successfully Activated !'}, status=status.HTTP_200_OK)
