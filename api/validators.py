import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value > dt.date.today().year:
        raise ValidationError(
            _('Вы ввели некорректное значение. Год не может быть больше '
              'текущего.'),
            params={'value': value},
        )
