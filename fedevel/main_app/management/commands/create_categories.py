from django.core.management import BaseCommand

from main_app.models import ProductCategory


class Command(BaseCommand):
    """Команда для создания категорий"""

    def handle(self, *args, **options):
        if not ProductCategory.objects.filter(is_active=True):
            categories = ['Футболки', 'Майки', 'Юбки', 'Платья', 'Кофты',
                          'Шорты', 'Носки']
            for category in categories:
                ProductCategory.objects.create(name=category,
                                               description='description',
                                               is_active=True)
