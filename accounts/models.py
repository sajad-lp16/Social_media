from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models

from utils.models import BaseModel
from .utils import file_handlers
from .utils import validators


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=150, unique=True, validators=[username_validator],
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _("A user with that username already exists."), }, )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to=file_handlers.rename_file, blank=True, null=True,
                               default='profiles/default_profile.png')
    bio = models.TextField(_('bio'), blank=True)
    phone_number = models.PositiveBigIntegerField(_('phone_number'), unique=True,
                                                  validators=[validators.phone_number_validator], error_messages={
            'unique': _("A user with that phone number already exists."), })
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': _("A user with that email already exists."), })
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ), )
    is_verified = models.BooleanField(_('is verified'), default=False)
    is_private = models.BooleanField(_('is private'), default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'Accounts'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
