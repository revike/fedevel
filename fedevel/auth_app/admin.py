from django.contrib import admin

from auth_app.models import ShopUser, ShopUserProfile


class UserInline(admin.StackedInline):
    model = ShopUserProfile
    extra = 1
    max_num = 1


class ShopUserAdmin(admin.ModelAdmin):
    inlines = (UserInline,)


admin.site.register(ShopUser, ShopUserAdmin)
admin.site.register(ShopUserProfile)
