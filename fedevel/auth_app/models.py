from datetime import timedelta

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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

    username = models.CharField(
        max_length=150, unique=True, verbose_name='username',
        validators=[UnicodeUsernameValidator()])
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    phone_regex = RegexValidator(regex=r'^\+7\d{10}$')
    phone = models.CharField(validators=[phone_regex], max_length=12,
                             blank=True, unique=False,
                             verbose_name='номер телефона')
    activation_key_email = models.CharField(max_length=128, blank=True)
    activation_key_phone = models.CharField(max_length=128, blank=True)
    activation_key_expires_email = models.DateTimeField(
        default=(now() + timedelta(hours=12)))
    activation_key_expires_phone = models.DateTimeField(
        default=(now() + timedelta(minutes=3)))
    is_active_email = models.BooleanField(default=True, db_index=True,
                                          verbose_name='активен email')
    is_active_phone = models.BooleanField(default=True, db_index=True,
                                          verbose_name='активен телефон')

    def is_activation_key_expired_email(self):
        if now() <= self.activation_key_expires_email:
            return False
        return True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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
                                db_index=True, primary_key=True,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='image_profile', blank=True, verbose_name='аватар')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=1, blank=True,
                              choices=GENDER_CHOICES, verbose_name='пол')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активен')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        try:
            img = Image.open(self.avatar.path)
            size = 200
            if img.height > size or img.width > size:
                output_size = (size, size)
                # img.thumbnail(output_size, Image.ANTIALIAS)
                # img.save(self.avatar.path)
                img_resize = img.resize(output_size)
                img_resize.show()
                img_resize.save(self.avatar.path)
        except ValueError:
            pass

    def __str__(self):
        return f'{self.user}'
