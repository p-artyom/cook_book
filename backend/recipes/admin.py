from django.contrib import admin

from core.admin import BaseAdmin
from recipes.models import Product, ProductInRecipe, Recipe


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'number_uses')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'created', 'modified')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(ProductInRecipe)
class ProductInRecipeAdmin(BaseAdmin):
    list_display = ('pk', 'recipe', 'product', 'weight')
    list_editable = ('recipe', 'product')
    search_fields = ('recipe', 'product')
