from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class RelationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relations'

    verbose_name = _('relation')
    verbose_name_plural = _('relations')

