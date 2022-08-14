from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from main_app.models import ProductOption, ProductCategory, Product


class IndexView(ListView):
    """Контроллер главной страницы"""
    model = ProductOption
    template_name = 'main_app/index.html'
    queryset = model.get_all_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.get_categories()
        context['title'] = 'главная'
        context['categories'] = categories
        return context


class ProductCategoryListView(ListView):
    """Контроллер продуктов категории"""
    template_name = 'main_app/products_category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.get_product_category(self.kwargs['pk'])
        categories = ProductCategory.get_categories()
        context['title'] = categories.get(pk=self.kwargs['pk']).name
        context['categories'] = categories
        context['products'] = products
        return context

    def get_queryset(self):
        return get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
