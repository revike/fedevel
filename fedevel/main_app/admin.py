from django.contrib import admin

from main_app.models import ProductCategory, Product, ProductOption, \
    ProductImage


class InlineProduct(admin.StackedInline):
    model = Product
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [InlineProduct]


class InlineOption(admin.TabularInline):
    model = ProductOption
    extra = 1


class InlineImage(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineOption, InlineImage]


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
