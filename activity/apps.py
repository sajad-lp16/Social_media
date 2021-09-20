from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity'

    verbose_name = _('activity')
    verbose_name_plural = _('activities')
