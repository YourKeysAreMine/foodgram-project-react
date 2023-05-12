# Generated by Django 4.2 on 2023-05-12 18:44

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите имя пользователя.Максимальная длина имени пользователя 150 символов.', max_length=150, unique=True, validators=[users.validators.validate_name], verbose_name='Имя пользователя'),
        ),
    ]
