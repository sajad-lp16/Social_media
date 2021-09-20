from oauth2_provider.views.mixins import OAuthLibMixin


class CustomOauthMixin(OAuthLibMixin):
    def create_token_response(self, request, refresh_token=None):
        core = self.get_oauthlib_core()
        return core.create_token_response(request, refresh_token=refresh_token)
