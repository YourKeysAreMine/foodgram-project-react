from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.models import Follow, User
from users.serializers import CustomUserSerializer

from .models import (FavoriteRecipe, IngredientRecipe, Recipe,
                     ShoppingCartRecipe)


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода количества ингредиентов
    будет применён в сериализаторе для отображения рецептов
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка рецептов
    """
    author = CustomUserSerializer(read_only=True)
    # Потестил с внутренним сериализатором, к сожалению, когда
    # я использую IngredientAmountSerializer(many=True) появляется
    # ошибка: AttributeError: Got AttributeError when attempting
    # to get a value for field `amount` on serializer
    # `IngredientAmountSerializer`. Original exception text was:
    # 'Ingredient' object has no attribute 'amount'.
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCartRecipe.objects.filter(
            user=user.id,
            recipe=obj.id
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления ингредиентов
    будет применяться в сериализаторе для добавления рецептов
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор отображения информации о подписке
    будет использоваться в сериализаторе для рецептов
    """

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.pk).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления и изменения рецептов
    """
    author = AuthorSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField()

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeListSerializer(
            instance,
            context={'request': request}
        )
        return serializer.data

    def ingredient_list_create(self, instance, ingredients):
        ingredients_list = [
            IngredientRecipe(
                recipe=instance,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ]
        return IngredientRecipe.objects.bulk_create(ingredients_list)

    def validate(self, data):
        ingredients = data.get('ingredients', None)
        tags = data.get('tags', None)
        if not ingredients:
            raise serializers.ValidationError(
                'Выберите хотя бы один ингредиент')
        elif not tags:
            raise serializers.ValidationError('Выберите хотя бы один тег')
        # Спасибо за ревью, к сожалению, когда я initial_data меняю
        # на data, появляется следующая ошибка: AssertionError: When a
        # serializer is passed a `data` keyword argument you must call
        # `.is_valid()` before attempting to access the serialized
        # `.data` representation. You should either call `.is_valid()`
        #  first, or access `.initial_data` instead.
        ingredient_data = self.initial_data.get('ingredients')
        if ingredient_data:
            checked_ingredients = set()
            for ingredient in ingredient_data:
                # К сожалению, когда я убираю дополнительную выборку ниже
                # и обращаюсь просто к ingredient
                # Возникает ошибка: TypeError: unhashable type: 'dict'
                ingredient_obj = get_object_or_404(
                    Ingredient, id=ingredient['id']
                )
                if ingredient_obj in checked_ingredients:
                    raise serializers.ValidationError(
                        'Выбирете другой ингредиент')
                checked_ingredients.add(ingredient_obj)
        return data

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = Recipe.objects.create(**validated_data)
        instance.tags.set(tags)
        self.ingredient_list_create(instance, ingredients)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.clear()
            self.ingredient_list_create(instance, ingredients)
        return instance

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения сведений о рецепте
    """
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
