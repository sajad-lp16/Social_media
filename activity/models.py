from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from utils.models import BaseModel
from social.models import Post
from .utils import functions
from chat.models import Message

User = get_user_model()


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    content = models.CharField(_('content'), max_length=300)
    slug = models.SlugField(_('slug'), max_length=150, blank=True, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('post'))
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('reply'), null=True, blank=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = functions.comment_slug(self)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        abstract = True


class LikeComment(Like, BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', verbose_name=_('comment'))

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Like_comments'
        verbose_name = _('Like_comment')
        verbose_name_plural = _('Like_comment')


class LikePost(Like, BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name=_('post'))

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Like_posts'
        verbose_name = _('Like_posts')
        verbose_name_plural = _('Like_posts')


class LikeMessage(Like, BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='likes', verbose_name=_('message'))

    def __str__(self):
        return self.user.__str__()

    class Meta:
        db_table = 'Like_messages'
        verbose_name = _('Like_message')
        verbose_name_plural = _('Like_messages')
