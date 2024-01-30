from django.urls import path

from api.views import add_product_to_recipe, cook_recipe

urlpatterns = [
    path('add_product_to_recipe/', add_product_to_recipe),
    path('cook_recipe/', cook_recipe),
]
