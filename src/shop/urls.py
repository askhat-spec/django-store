from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='main'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/<slug:slug>', views.product_detail, name='product_detail'),
]