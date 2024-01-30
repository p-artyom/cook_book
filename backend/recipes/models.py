from behaviors.behaviors import Timestamped
from django.core.validators import MinValueValidator
from django.db import models

from core.models import NameModel
from core.utils import cut_string


class Product(NameModel):
    number_uses = models.IntegerField(
        'количество приготовленных блюд с использованием этого продукта',
        default=0,
        validators=[MinValueValidator(0)],
        help_text=(
            'Введите количество приготовленных блюд с '
            'использованием этого продукта'
        ),
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self) -> str:
        return cut_string(self.name)


class Recipe(NameModel, Timestamped):
    products = models.ManyToManyField(
        Product,
        through='ProductInRecipe',
        verbose_name='список продуктов',
        help_text='Выберите продукты',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-created',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('created').verbose_name = 'дата публикации'
        self._meta.get_field('modified').verbose_name = 'дата изменения'

    def __str__(self) -> str:
        return cut_string(self.name)


class ProductInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберите рецепт',
    )
    product = models.ForeignKey(
        Product,
        related_name='product_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='продукт',
        help_text='Выберите продукт',
    )
    weight = models.IntegerField(
        'вес в граммах',
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Введите вес в граммах',
    )

    class Meta:
        verbose_name = 'продукт в рецепт'
        verbose_name_plural = 'продукты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'product'],
                name='unique_products',
            ),
        ]

    def __str__(self):
        return f'В рецепт `{self.recipe}` входит `{self.product}`'
