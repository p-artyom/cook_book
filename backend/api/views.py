from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Product, ProductInRecipe, Recipe


@extend_schema(
    summary='Добавить к рецепту указанный продукт с указанным весом',
    description='Добавляет к рецепту указанный продукт с указанным весом',
    parameters=[
        OpenApiParameter(
            name='recipe_id',
            description='Идентификатор рецепта',
            type=int,
            required=True,
        ),
        OpenApiParameter(
            name='product_id',
            description='Идентификатор продукта',
            type=int,
            required=True,
        ),
        OpenApiParameter(
            name='weight',
            description='Вес продукта в граммах',
            type=int,
            required=True,
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response={
                'example': {
                    'message': (
                        'К рецепту `Сырник` добавлен продукт `Яйцо` с '
                        'указанным весом'
                    ),
                },
            },
        ),
    },
)
@api_view(['GET'])
def add_product_to_recipe(request: HttpRequest) -> HttpResponse:
    recipe = get_object_or_404(
        Recipe,
        id=request.query_params.get('recipe_id'),
    )
    product = get_object_or_404(
        Product,
        id=request.query_params.get('product_id'),
    )
    product_in_recipe, _ = ProductInRecipe.objects.get_or_create(
        recipe=recipe,
        product=product,
    )
    product_in_recipe.weight = request.query_params.get('weight')
    product_in_recipe.save()
    return Response(
        {
            'message': (
                f'К рецепту `{recipe.name}` добавлен продукт '
                f'`{product.name}` с указанным весом'
            ),
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    summary='Увеличить количество приготовленных блюд для каждого продукта',
    description=(
        'Увеличивает количество приготовленных блюд для каждого продукта'
    ),
    parameters=[
        OpenApiParameter(
            name='recipe_id',
            description='Идентификатор рецепта',
            type=int,
            required=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={
                'example': {
                    'message': (
                        'Количество приготовленных блюд для каждого '
                        'продукта увеличено'
                    ),
                },
            },
        ),
    },
)
@api_view(['GET'])
def cook_recipe(request: HttpRequest) -> HttpResponse:
    recipe = get_object_or_404(
        Recipe,
        id=request.query_params.get('recipe_id'),
    )
    products_in_recipe = ProductInRecipe.objects.filter(recipe=recipe)
    if not products_in_recipe:
        return Response(
            {'message': f'Рецепт `{recipe.name}` не содержит продукты'},
            status=status.HTTP_404_NOT_FOUND,
        )
    for product_in_recipe in products_in_recipe:
        product = Product.objects.get(id=product_in_recipe.product.id)
        product.number_uses += 1
        product.save()
    return Response(
        {
            'message': (
                'Количество приготовленных блюд для каждого продукта увеличено'
            ),
        },
        status=status.HTTP_200_OK,
    )
