from django.urls import path
from auth_app import views as auth_app

app_name = 'auth_app'

urlpatterns = [
    path('login/', auth_app.LoginUserView.as_view(), name='login'),
    path('logout/', auth_app.LogoutUserView.as_view(), name='logout'),
    path('register/', auth_app.RegisterView.as_view(), name='register'),
    path('verify/<email>/<activation_key>/', auth_app.VerifyView.as_view(),
         name='verify')
]
