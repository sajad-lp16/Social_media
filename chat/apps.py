from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    verbose_name = _('chat')
    verbose_name_plural = _('chats')

