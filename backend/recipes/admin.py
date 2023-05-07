from django.contrib import admin

from .models import (FavoriteRecipe, IngredientRecipe, Recipe,
                     ShoppingCartRecipe, TagRecipe)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 0


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1
    extra = 0


class FavoriteRecipeInLine(admin.TabularInline):
    model = FavoriteRecipe
    extra = 0


class ShoppingCartRecipeInLine(admin.TabularInline):
    model = ShoppingCartRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInline,
        TagInline,
        FavoriteRecipeInLine,
        ShoppingCartRecipeInLine,
    )
    list_display = (
        'id',
        'name',
        'author',
        'number_of_favorites',
        )
    search_fields = ('author', 'name', 'tags',)
    list_filter = ('author', 'name', 'tags',)

    @staticmethod
    def number_of_favorites(obj):
        return obj.fav_recipe.count()


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(TagRecipe)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCartRecipe)
