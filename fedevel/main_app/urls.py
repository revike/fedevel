from django.urls import path
from main_app import views as main_app

app_name = 'main_app'

urlpatterns = [
    path('', main_app.IndexView.as_view(), name='index'),
    path('<int:pk>/', main_app.ProductCategoryListView.as_view(),
         name='category'),
]
