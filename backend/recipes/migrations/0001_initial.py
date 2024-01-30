import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=200,
                        verbose_name="название",
                    ),
                ),
                (
                    "number_uses",
                    models.IntegerField(
                        default=0,
                        help_text=(
                            "Введите количество приготовленных блюд с "
                            "использованием этого продукта"
                        ),
                        validators=[
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name=(
                            "количество приготовленных блюд с "
                            "использованием этого продукта"
                        ),
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
        migrations.CreateModel(
            name="ProductInRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=1,
                        help_text="Введите вес в граммах",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="вес в граммах",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Выберите продукт",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_in_recipe",
                        to="recipes.product",
                        verbose_name="продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт в рецепт",
                "verbose_name_plural": "продукты в рецептах",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=200,
                        verbose_name="название",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        help_text="Выберите продукты",
                        through="recipes.ProductInRecipe",
                        to="recipes.product",
                        verbose_name="список продуктов",
                    ),
                ),
            ],
            options={
                "verbose_name": "рецепт",
                "verbose_name_plural": "рецепты",
                "ordering": ("-created",),
            },
        ),
        migrations.AddField(
            model_name="productinrecipe",
            name="recipe",
            field=models.ForeignKey(
                help_text="Выберите рецепт",
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
                verbose_name="рецепт",
            ),
        ),
        migrations.AddConstraint(
            model_name="productinrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "product"),
                name="unique_products",
            ),
        ),
    ]
