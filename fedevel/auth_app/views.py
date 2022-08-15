from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from auth_app.forms import CompanyUserLoginForm
from main_app.models import ProductCategory


class LoginUserView(LoginView):
    """Контроллер авторизации Login ShopUser"""
    template_name = 'auth_app/login.html'
    form_class = CompanyUserLoginForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        context = super().get_context_data(**kwargs)
        context['title'] = 'вход'
        context['categories'] = ProductCategory.get_categories()
        return context

    def form_valid(self, form):
        next_url = self.request.session['next_url']
        email = self.request.POST.get('email')
        password = self.request.POST['password']
        auth.authenticate(email=email, password=password)
        login(self.request, form.get_user())
        if next_url:
            return HttpResponseRedirect(self.request.session['next_url'])
        return HttpResponseRedirect(reverse('main:index'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:index'))
        return super().get(self.request, **kwargs)


class LogoutUserView(LogoutView):
    """Logout CompanyUser"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('auth:login'))
