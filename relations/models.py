from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from utils.models import BaseModel

User = get_user_model()


class Relation(BaseModel):
    start_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings', verbose_name=_('start user'))
    end_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name=_('end user'))

    class Meta:
        db_table = 'Relations'
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')
        unique_together = [('start_user', 'end_user')]

    def __str__(self):
        return f'{self.start_user} -> {self.end_user}'

    def clean(self):
        if self.start_user == self.end_user:
            raise ValidationError('Users cant be the same!')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
