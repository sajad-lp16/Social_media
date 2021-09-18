import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from oauth2_provider.models import get_access_token_model
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.signals import app_authorized
from oauthlib.common import urlencode

User = get_user_model()


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        user = User.objects.filter(
            Q(username=username) | Q(email=username)
        ).first()
        if user is None:
            try:
                user = User.objects.filter(phone_number=username).first()
            except (ValueError, TypeError):
                return

        if user.check_password(password) and self.user_can_authenticate(user):
            return user


class UserOAuthLibCore(OAuthLibCore):

    def _extract_params(self, request, refresh_token=None):
        uri = self._get_escaped_full_path(request)
        http_method = request.method
        headers = self.extract_headers(request)
        body = urlencode(self.extract_body(request, refresh_token=refresh_token))
        return uri, http_method, body, headers

    def create_token_response(self, request, refresh_token=None):

        uri, http_method, body, headers = self._extract_params(request, refresh_token=None)
        extra_credentials = self._get_extra_credentials(request)

        headers, body, status = self.server.create_token_response(
            uri, http_method, body, headers, extra_credentials
        )
        uri = headers.get("Location", None)

        return uri, headers, body, status

    def extract_body(self, request, refresh_token=None):
        try:
            body = json.loads(request.body.decode("utf-8"))
            body['client_id'] = settings.CLIENT_ID
            body['grant_type'] = 'password'
            if refresh_token is not None:
                body['grant_type'] = 'refresh_token'
                body['refresh_token'] = refresh_token
            body = body.items()
        except AttributeError:
            body = ""
        except ValueError:
            body = ""

        return body


def handle_token_creation(obj, request, headers, body, status):
    if status == 200:
        access_token = json.loads(body).get("access_token")
        if access_token is not None:
            token = get_access_token_model().objects.get(token=access_token)
            app_authorized.send(sender=obj, request=request, token=token)
    response = HttpResponse(content=body, status=status)

    for k, v in headers.items():
        response[k] = v
    return response
