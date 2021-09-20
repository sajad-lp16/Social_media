from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class SocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social'

    verbose_name = _('social')
    verbose_name_plural = _('social')
