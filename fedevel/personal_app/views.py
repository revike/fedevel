from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main_app.models import ProductCategory


class MainPageView(TemplateView):
    """Контроллер главное страницы личного кабинета"""
    template_name = 'personal_app/main_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.get_categories()
        context['title'] = 'личный кабинет'
        context['categories'] = categories
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
