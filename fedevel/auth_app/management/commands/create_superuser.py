from django.core.management import BaseCommand
from auth_app.models import ShopUser


class Command(BaseCommand):
    """Команда для создания супер юзера"""

    def handle(self, *args, **options):
        admin_email = 'email@email.local'
        if not ShopUser.objects.filter(is_staff=True, is_active=True):
            ShopUser.objects.create_superuser(
                username='admin', email=admin_email, password='admin',
                last_name='admin', first_name='admin'
            )
