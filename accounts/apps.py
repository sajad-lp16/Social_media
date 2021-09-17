from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    verbose_name = _('account')
    verbose_name_plural = _('accounts')
