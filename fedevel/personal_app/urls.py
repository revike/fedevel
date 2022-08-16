from django.urls import path
from personal_app import views

app_name = 'personal_app'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main')
]
