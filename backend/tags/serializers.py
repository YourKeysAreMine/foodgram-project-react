from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов
    """
    class Meta:
        model = Tag
        fields = '__all__'
