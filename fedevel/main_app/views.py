from django.views.generic import ListView
from main_app.models import ProductOption


class IndexView(ListView):
    """Главная страница"""
    model = ProductOption
    template_name = 'main_app/index.html'
    queryset = model.get_all_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная'
        return context
