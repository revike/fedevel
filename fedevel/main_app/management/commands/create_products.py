from django.core.management import BaseCommand

from main_app.models import Product, ProductCategory


class Command(BaseCommand):
    """Команда для создания категорий"""

    def handle(self, *args, **options):
        if not Product.objects.filter(is_active=True):
            categories = ProductCategory.objects.all()
            for category in categories:
                products_name = [f'одуванчик {category.name}',
                                 f'бабочка {category.name}',
                                 f'светофор {category.name}']
                for product in products_name:
                    Product.objects.create(
                        category_id=category.id,
                        name=product,
                        short_desc=f'краткое описание {product}',
                        description=f'описание {product}',
                        is_active=True
                    )
