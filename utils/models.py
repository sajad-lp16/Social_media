from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        abstract = True
