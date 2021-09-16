import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def phone_number_validator(value):
    regex = r'^989[0-3][\d]{8}$'
    if re.match(regex, str(value)) is None:
        raise ValidationError(
            _(f'{value} is not a valid phone number.'),
            params={'value': value}
        )