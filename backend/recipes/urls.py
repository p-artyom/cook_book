from django.urls import path

from recipes.views import show_recipes_without_product

urlpatterns = [
    path('show_recipes_without_product/', show_recipes_without_product),
]
