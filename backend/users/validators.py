from django.core.exceptions import ValidationError


def validate_name(value):
    # Действительно, была небольшая ошибка, плюс я забыл добавить валидатор
    # в поле 'uesrname' модели User :)
    if value != 'me':
        return value
    else:
        raise ValidationError(
            f'Использовать имя {value} в качестве имя пользователя запрещено!'
        )
