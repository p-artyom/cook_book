from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view

from recipes.models import Product, Recipe


@extend_schema(
    summary='Получить HTML страницу, на которой размещена таблица с рецептами',
    description=(
        'Возвращает HTML страницу, на которой размещена таблица с рецептами. '
        'В таблице отображены ID и названия всех рецептов, в которых '
        'указанный продукт отсутствует, или присутствует в количестве меньше '
        '10 грамм.'
    ),
    parameters=[
        OpenApiParameter(
            name='product_id',
            description='Идентификатор продукта',
            type=int,
            required=True,
        ),
    ],
)
@api_view(['GET'])
def show_recipes_without_product(request: HttpRequest) -> HttpResponse:
    selected_product = get_object_or_404(
        Product,
        id=request.query_params.get('product_id'),
    )
    return render(
        request,
        'recipes.html',
        {
            'recipes': Recipe.objects.filter(
                ~Q(productinrecipe__product=selected_product)
                | (
                    Q(productinrecipe__product=selected_product)
                    & Q(productinrecipe__weight__lte=10)
                ),
            ).distinct(),
        },
    )
