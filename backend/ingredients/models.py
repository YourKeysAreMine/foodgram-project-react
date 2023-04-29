from django.db import models


class Ingredient(models.Model):
    """
    Модель ингредиентов
    """
    name = models.CharField(
        verbose_name="Наименование ингредиента",
        max_length=250,
        help_text="Введите название ингредиента",
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения",
        max_length=250,
        help_text="Введите единицу измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f"{self.name} {self.measurement_unit}"
