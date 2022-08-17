from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView

from auth_app.models import ShopUserProfile
from main_app.models import ProductCategory
from personal_app.forms import ProfileEditForm, ShopUserEditForm


class MainPageView(TemplateView):
    """Контроллер главной страницы личного кабинета"""
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


class ProfileUpdateView(UpdateView):
    """Контроллер профиля"""
    template_name = 'personal_app/profile.html'
    model = ShopUserProfile
    form_class = ProfileEditForm
    form_user = ShopUserEditForm
    success_url = reverse_lazy('personal:main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form_user = self.form_user(instance=self.request.user)
        categories = ProductCategory.get_categories()
        context['title'] = f'профиль'
        context['categories'] = categories
        context['form_user'] = form_user
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form_user = self.form_user(self.request.POST,
                                   instance=self.request.user)
        if form.is_valid() and form_user.is_valid():
            self.form_valid(form)
            self.form_valid(form_user)
        return HttpResponseRedirect(
            reverse('personal:profile', kwargs={'pk': self.request.user.pk}))

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
