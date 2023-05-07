from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    """
    Модель тега
    """
    REQUIRED_FIELDS = ["name",
                       "color",
                       "slug"]
    name = models.CharField(
        verbose_name="Название",
        unique=True,
        max_length=150,
        help_text="Введите название тэга",
    )
    color = models.CharField(
        verbose_name="Цвет",
        unique=True,
        max_length=7,
        help_text="Введите цветовой HEX-код в формате #xxxxxx",
        validators=[
            RegexValidator(
                regex=r"^#[a-fA-F0-9]{6}$",
                message="Введите цветовой HEX-код в формате #xxxxxx",
            )
        ],
    )
    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
        max_length=30,
        help_text="Введите slug",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
