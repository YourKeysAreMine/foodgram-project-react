# Generated by Django 4.2 on 2023-05-13 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0004_alter_shoppingcartrecipe_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientrecipes', to='ingredients.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientrecipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
