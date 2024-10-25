import re
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    if not bool(re.match(pattern, field)):
        print('Must contain A-Z, a-z letters and 0-9 numbers')
        raise ValidationError('Пароль должен содержать символы латинского алфавита и цифры!')
    if not 8 <= len(field) <= 12:
        print('Password length must be between 8 and 12 characters')
        raise ValidationError('Длина пароля должна быть между 8 и 12 символов')
