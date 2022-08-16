from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from auth_app.forms import CompanyUserLoginForm, CompanyUserRegisterForm
from auth_app.models import ShopUser
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


class RegisterView(CreateView):
    """Контроллер регистрации"""
    template_name = 'auth_app/register.html'
    form_class = CompanyUserRegisterForm
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        context['title'] = 'Регистрация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:index'))
        return super().get(self.request, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active_email = False
            user.is_active_phone = False
            user.save()

            username = user.username
            password = self.request.POST['password2']
            login_user = auth.authenticate(username=username, password=password)
            login(self.request, login_user)

            return HttpResponseRedirect(reverse('auth:login'))


class VerifyView(TemplateView):
    """Контроллер верификации"""
    template_name = 'auth_app/verification.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'верификация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        user = ShopUser.objects.filter(
            email=self.kwargs['email'],
            activation_key_email=self.kwargs['activation_key_email']).first()
        try:
            if user.activation_key_email == self.kwargs[
                'activation_key_email']:
                if not user.is_activation_key_expired_email():
                    user.activation_key_email = ''
                    user.is_active_email = True
                    user.save()
                    auth.login(request, user)
                    return super().get(self.request)
        except AttributeError:
            ...
        return HttpResponseRedirect(reverse('main:index'))
