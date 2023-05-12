# Generated by Django 4.2 on 2023-05-12 16:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Любимый рецепт',
                'verbose_name_plural': 'Любимые рецепты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество ингредиента')),
            ],
            options={
                'verbose_name': 'Ингредиент: Рецепт',
                'verbose_name_plural': 'Ингредиенты: Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Текущая дата и время устанавливается автоматически', verbose_name='Дата создания')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=150, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Загрузите картинку', upload_to='recipes/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Введите описание рецепта', verbose_name='Текстовое описание')),
                ('cooking_time', models.IntegerField(help_text='Введите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, message='Укажите число больше либо равное 1')], verbose_name='Время приготовления в минутах')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe', to='recipes.recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='tags.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег: Рецепт',
                'verbose_name_plural': 'Теги: Рецепты',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCartRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Рецепт в корзине пользователя',
                'verbose_name_plural': 'Рецепты в корзине пользователя',
            },
        ),
    ]
