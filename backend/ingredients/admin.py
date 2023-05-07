from django.contrib import admin

from .models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']


admin.site.register(Ingredient, IngredientAdmin)
