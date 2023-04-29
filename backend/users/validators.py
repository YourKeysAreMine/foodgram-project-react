from rest_framework import serializers


def validate_name(value):
    me = 'me'
    if value == me:
        raise serializers.ValidationError(
            f'Использовать имя {value} в качестве имя пользователя запрещено!'
        )
