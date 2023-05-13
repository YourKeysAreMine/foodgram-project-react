from django.core.exceptions import ValidationError


def validate_name(value):
    if value != 'me':
        return value
    raise ValidationError(
        f'Использовать имя {value} в качестве имя пользователя запрещено!'
    )
