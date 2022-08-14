from datetime import timedelta
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ShopUser(AbstractUser):
    """Модель пользователя"""

    class Meta:
        verbose_name_plural = 'пользователи'
        verbose_name = 'пользователи'

    email = models.EmailField(_("email address"), blank=True)
    phone_regex = RegexValidator(regex=r'^\+7\d{10}$')
    phone = models.CharField(validators=[phone_regex], max_length=12,
                             blank=True, verbose_name='номер телефона')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        return True

    def __str__(self):
        return f'{self.first_name} {self.last_name} "{self.username}"'


class ShopUserProfile(models.Model):
    """Профиль пользователя"""
    class Meta:
        verbose_name_plural = 'профиль пользователя'
        verbose_name = 'профиль пользователя'

    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False,
                                db_index=True, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='image_profile', blank=True, verbose_name='аватар')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=1, blank=True,
                              choices=GENDER_CHOICES, verbose_name='пол')
    is_active = models.BooleanField(default=False, db_index=True,
                                    verbose_name='активен')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        try:
            img = Image.open(self.avatar.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save()
        except (TypeError, ValueError):
            pass

    def __str__(self):
        return f'{self.user}'
