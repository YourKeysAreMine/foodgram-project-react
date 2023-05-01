from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка ингредиентов
    """
    class Meta:
        model = Ingredient
        fields = '__all__'
