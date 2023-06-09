# Generated by Django 4.2 on 2023-05-16 09:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество ингредиентов не может быть меньше 1')], verbose_name='Количество ингредиента'),
        ),
    ]
