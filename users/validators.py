import re
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_message = [
        {'ru-ru': "Пароль должен содержать символы латинского алфавита или цифры",
         'en-us': "Password must contain alphanumeric characters"},
        {'ru-ru': "Длинна пароля должны быть от 8 до 16 символов",
         'en-us': "Password lenght must be between 8 and 16 charters"}
    ]

    if not bool(re.match(pattern, field)):
        print(error_message[0][language])
        raise ValidationError(error_message[0][language],
                              code=error_message[0][language])
    if not 8 <= len(field) <= 16:
        print(error_message[1][language])
        raise ValidationError(error_message[1][language],
                              code=error_message[0][language])
