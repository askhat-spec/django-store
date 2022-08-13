from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='main'),
    path('shop/', views.ProductList.as_view(), name='product_list'),
    path('shop/<slug:slug>', views.product_detail, name='product_detail'),
    path('about', views.about, name='about'),
    path('info', views.info, name='info'),
    path('search', views.Search.as_view(), name='search'),
]