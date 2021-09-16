from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from utils.models import BaseModel
from .utils import functions

User = get_user_model()


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('user'))
    caption = models.CharField(_('caption'), max_length=300, blank=True)
    slug = models.SlugField(_('slug'), max_length=150, blank=True, unique=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Post'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = functions.post_slug(self)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Media(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media', verbose_name=_('user'), blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media', verbose_name=_('post'))
    media = models.FileField(verbose_name=_('media'), upload_to=functions.rename_file,
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['jpg', 'mkv', 'mp4', 'flv', 'avi', 'png', 'jpeg'])])

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Media'
        verbose_name = _('Media')
        verbose_name_plural = _('Media')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        self.user = self.post.user
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
