from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.models import BaseModel
from .utils import functions

User = get_user_model()


class Conversation(BaseModel):
    start_user = models.ForeignKey(User, related_name='chat_start', on_delete=models.CASCADE, verbose_name=_('user'))
    end_user = models.ForeignKey(User, related_name='chat_end', on_delete=models.CASCADE, verbose_name=_('user'))
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_('slug'), blank=True)

    def __str__(self):
        return f'{self.start_user.__str__()} and {self.end_user.__str__()}'

    class Meta:
        db_table = 'ChatRoom'
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        unique_together = [('start_user', 'end_user')]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = functions.conversation_slug(self)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Message(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='messages')
    media = models.FileField(verbose_name=_('media'), upload_to=functions.rename_file,
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['jpg', 'mkv', 'mp4', 'flv', 'avi', 'png', 'jpeg'])])

    content = models.CharField(_('content'), max_length=200)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                     verbose_name=_('conversation'), related_name='messages')

    def __str__(self):
        return f'{self.user.__str__()} to {self.conversation.end_user.__str__()}'

    class Meta:
        db_table = 'messages'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
