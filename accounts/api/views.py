import json

from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.views import TokenView

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as response_status

from . import serializers
from ..utils.authentication_backend import handle_token_creation, restrict_invalid_request
from ..utils.oauth_mixin import CustomOauthMixin
from ..utils.permissions import AccountOwnerPermission
from ..utils.verification_backend import generate_code
from ..utils.verification_backend import send_verification_email
from ..utils.verification_backend import send_verification_sms

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = AllowAny,


@method_decorator(csrf_exempt, name="dispatch")
class RegisterUser(CustomOauthMixin, View):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        if request.GET.get('access_token'):
            return restrict_invalid_request()
        data = json.loads(request.body)
        serializer = serializers.UserSerializer(data=data)
        if not serializer.is_valid():
            return HttpResponse(content=json.dumps(serializer.errors), content_type='application/json')
        serializer.save()
        url, headers, body, status = self.create_token_response(request)
        return handle_token_creation(self, request, headers, body, status)


@method_decorator(csrf_exempt, name="dispatch")
class LoginUser(CustomOauthMixin, View):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        if request.GET.get('access_token'):
            return restrict_invalid_request()
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        refresh_token = None
        if user is None:
            return HttpResponse(content=json.dumps(
                {'message': 'Invalid Credentials'}),
                status=response_status.HTTP_404_NOT_FOUND,
                content_type='application/json'
            )
        try:
            token = user.oauth2_provider_accesstoken.get_queryset().last()
            refresh_token = token.refresh_token
            if token.is_valid():
                return HttpResponse(content=json.dumps(
                    {'token': token.token, 'refresh_token': refresh_token.token}),
                    content_type='application/json',
                    status=response_status.HTTP_200_OK
                )
        except AttributeError:
            pass

        url, headers, body, status = self.create_token_response(request, refresh_token=refresh_token)
        return handle_token_creation(self, request, headers, body, status)


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
            return Response({'message': 'Activation Code Was Sent To Your Phone'}, status=response_status.HTTP_200_OK)
        send_verification_email.delay(request.user.email, code)
        cache.set(key_code, code, timeout=90)
        return Response({'message': 'Activation Code Was Sent To Your Email'}, status=response_status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        submit_code = request.data.get('code')
        auth_code = cache.get(f'{user.username}')
        if auth_code is None:
            return Response({'message': 'The Code Is Invalid Or Expired'}, status=response_status.HTTP_404_NOT_FOUND)
        if auth_code != submit_code:
            return Response({'message': 'The Code Is Invalid !'}, status=response_status.HTTP_403_FORBIDDEN)
        user.is_verified = True
        user.save()
        return Response({'message': 'The Account Has Been Successfully Activated !'},
                        status=response_status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class RefreshTokenAPIView(CustomOauthMixin, View):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        url, headers, body, status = self.create_token_response(request, refresh_token=refresh_token)
        return handle_token_creation(self, request, headers, body, status)
