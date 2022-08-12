from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ProductCategory(models.Model):
    """Категории продуктов"""

    class Meta:
        verbose_name_plural = 'категории продуктов'
        verbose_name = 'категории продуктов'

    name = models.CharField(max_length=64, unique=True,
                            verbose_name='название категории')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    @classmethod
    def get_categories(cls):
        return cls.objects.filter(is_active=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Модель продукта"""

    class Meta:
        verbose_name_plural = 'продукты'
        verbose_name = 'продукты'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 db_index=True,
                                 verbose_name='категория')
    name = models.CharField(max_length=64, verbose_name='название')
    short_desc = models.CharField(max_length=64,
                                  verbose_name='краткое описание')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    def __str__(self):
        return f'{self.name}; Категория: {self.category.name}'


class ProductOption(models.Model):
    """Опции продукта"""

    class Meta:
        verbose_name_plural = 'опции продукта'
        verbose_name = 'опции продукта'

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                db_index=True, verbose_name='продукт',
                                related_name='product_option')
    color = models.CharField(max_length=64, verbose_name='цвет')
    size = models.CharField(max_length=64, verbose_name='размер')
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        validators=[MinValueValidator(Decimal('0.00'))], verbose_name='цена')
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name='количество на складе')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    @classmethod
    def get_all_products(cls):
        return cls.objects.filter(
            is_active=True, product__is_active=True,
            product__category__is_active=True).select_related(
            'product', 'product__category')

    def __str__(self):
        return f'{self.product.name}'


class ProductImage(models.Model):
    """Фото продукта"""

    class Meta:
        verbose_name_plural = 'фото продукта'
        verbose_name = 'фото продукта'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_image',
        db_index=True, verbose_name='продукт')
    image = models.ImageField(
        upload_to=f'products_images/', blank=True,
        verbose_name='картинка')

    def __str__(self):
        return f'{self.product.name}'
