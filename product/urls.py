from django.urls import path

from . import views


app_name = 'product'

urlpatterns = [
    path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.ProductListView.as_view(), name='shop'),
]
