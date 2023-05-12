import json

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    """Manage - комманда для импорта ингредиентов из файла ingredients.json"""
    def handle(self, *args, **options):
        with open('ingredients.json', encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())
            for ingredient_data in json_data:
                Ingredient.objects.get_or_create(**ingredient_data)
