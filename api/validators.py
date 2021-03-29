import datetime as dt

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > dt.date.today().year:
        raise ValidationError(
            ('Вы ввели некорректное значение. Год не может быть больше '
             'текущего.'),
            params={'value': value},
        )
