from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow, User

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для получения списка пользователей.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class RecipeSerializerForFollow(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов в подписках
    """
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления и удаления подписок
    """
    email = serializers.CharField(
        source='author.email',
        read_only=True)
    id = serializers.IntegerField(
        source='author.id',
        read_only=True)
    username = serializers.CharField(
        source='author.username',
        read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipes.count')

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count',)

    def validate(self, data):
        user = self.context.get('request').user
        author = self.context.get('author_id')
        if user.id == int(author):
            raise serializers.ValidationError({
                'errors': 'Нельзя подписаться на самого себя'})
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписались на этого пользователя'})
        return data

    def get_recipes(self, obj):
        author = self.context.get('author_id')
        recipes = Recipe.objects.filter(author=author)
        return RecipeSerializerForFollow(
            recipes,
            many=True).data

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context.get('request').user,
            author=obj.author
        ).exists


class SubscriptionListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения подписок.
    КОММЕНТАРИЙ ДЛЯ РЕВЬЮЕРА! Привет, ни в какую не получается сделать
    GET /api/users/subscriptions. Postman возвращает 404, без дебаг сообщений,
    просто "detail": "not found". Docker тоже дебаг сообщений не выдаёт.
    Помоги пожалуйста, переписывал уже раз пять.
    Создавал два треда, именно по этому вопросу никто не помог...
    Причём, что интересно, при подписке по эндпоинту
    POST /api/users/user_id/sibscribe. Postman возвращает ответ согласно ТЗ.
    То есть ошибки в сериализаторе быть не может, так как сериализатор выше,
    специально для ПОСТ запросов для добавления подписок, который
    я писал заново - работает.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Follow.objects.filter(user=self.context['request'].user,
                                      author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializerForFollow(recipes, many=True,
                                               read_only=True)
        return serializer.data
