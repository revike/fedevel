from auth_app.models import ShopUser
from django.db.models import Q


class AuthBackend:
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return ShopUser.objects.get(pk=user_id)
        except ShopUser.DoesNotExist:
            return None

    def authenticate(self, request, username, password):

        try:
            user = ShopUser.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username))

        except ShopUser.MultipleObjectsReturned:
            users = ShopUser.objects.filter(email=username)
            for user in users:
                if user.is_active_email:
                    if user.check_password(password):
                        return user
            users = ShopUser.objects.filter(phone=username)
            for user in users:
                if user.is_active_phone:
                    if user.check_password(password):
                        return user
            return

        except ShopUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        else:
            return None
