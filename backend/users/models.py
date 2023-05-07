from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        help_text=(
            "Введите имя пользователя."
            "Максимальная длина имени пользователя 150 символов."
        )
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=150,
        unique=True,
        help_text=(
            "Введите адрес электронной почты"
        )
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        help_text="Введите имя",
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        help_text="Введите фамилию",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """
    Модель подписки на пользователя
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="follower",
        help_text="Выберите пользователя",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписка",
        related_name="following",
        help_text="Выберите автора",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique subscription')
        ]

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
