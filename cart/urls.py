from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('append-product/', views.append_product_to_cart, name='append_product_to_cart'),
    path('delete-product/', views.delete_product_from_cart, name='delete_product_from_cart'),
    path('change-product/', views.change_cartitem_quantity, name='change_cartitem_quantity'),
    path('clean/', views.clean_cart, name='clean_cart'),
    path('', views.cart_view, name='cart_view'),
]
