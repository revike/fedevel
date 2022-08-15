from django.urls import path
from auth_app import views as auth_app

app_name = 'auth_app'

urlpatterns = [
    path('login/', auth_app.LoginUserView.as_view(), name='login'),
    path('logout/', auth_app.LogoutUserView.as_view(), name='logout'),
]
