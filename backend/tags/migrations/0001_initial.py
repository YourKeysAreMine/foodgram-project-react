# Generated by Django 4.2 on 2023-05-12 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название тэга', max_length=150, unique=True, verbose_name='Название')),
                ('color', models.CharField(help_text='Введите цветовой HEX-код в формате #xxxxxx', max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Введите цветовой HEX-код в формате #xxxxxx', regex='^#[a-fA-F0-9]{6}$')], verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Введите slug', max_length=30, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
    ]
