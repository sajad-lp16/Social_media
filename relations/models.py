from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from utils.models import BaseModel

User = get_user_model()


class Relation(BaseModel):
    start_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings', verbose_name=_('user'))
    end_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name=_('user'))

    class Meta:
        db_table = 'Relations'
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')
        unique_together = [('start_user', 'end_user')]

    def __str__(self):
        return f'{self.start_user} -> {self.end_user}'
