from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка тегов
    """
    class Meta:
        model = Tag
        fields = '__all__'
