from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """
    Модель рецептов
    """
    created = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        help_text="Текущая дата и время устанавливается автоматически",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        verbose_name="Автор публикации",
        help_text="Укажите автора",
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=150,
        help_text="Введите название рецепта",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="recipes/",
        help_text="Загрузите картинку",
    )
    text = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        verbose_name="Ингредиенты",
        help_text="Выберите ингредиенты из списка",
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagRecipe",
        verbose_name="Теги",
        help_text="Выберите теги из списка",
    )
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Введите время приготовления в минутах",
        validators=[
            MinValueValidator(1, message="Укажите число больше либо равное 1"),
        ],
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-created",)

    def __str__(self):
        return f"{str(self.name)} {str(self.author)}"


class IngredientRecipe(models.Model):
    """
    Модель, связывающая рецепт и ингредиент
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredientrecipes",
        verbose_name="Ингредиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredientrecipes",
        verbose_name="Рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиента",
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов не может быть меньше 1'
            )
        ]
    )

    class Meta:
        verbose_name = "Ингредиент: Рецепт"
        verbose_name_plural = "Ингредиенты: Рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique ingredient amount',
            ),
        )

    def __str__(self):
        return f"{str(self.ingredient)}: {str(self.recipe)}"


class TagRecipe(models.Model):
    """
    Модель, связывающая тег и рецепт
    """
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="recipe_tag",
        verbose_name="Тег",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="tag_recipe",
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_tag_recipe",
                fields=["tag", "recipe"],
            ),
        ]
        verbose_name = "Тег: Рецепт"
        verbose_name_plural = "Теги: Рецепты"

    def __str__(self):
        return f"{str(self.tag)}: {str(self.recipe)}"


class FavoriteRecipe(models.Model):
    """
    Избранные рецепты
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="fav_recipe",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_fav_recipe",
        verbose_name="Пользователь",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_favorite_recipe",
                fields=["recipe", "user"],
            ),
        ]
        verbose_name = "Любимый рецепт"
        verbose_name_plural = "Любимые рецепты"


class ShoppingCartRecipe(models.Model):
    """
    Список покупок
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Пользователь",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_shopping_cart",
                fields=["recipe", "user"],
            ),
        ]
        verbose_name = "Рецепт в корзине пользователя"
        verbose_name_plural = "Рецепты в корзине пользователя"
