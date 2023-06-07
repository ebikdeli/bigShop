from django.urls import path

from . import views


app_name = 'order'

urlpatterns = [
    path('order-form/', views.order_form, name='order-form'),
    path('checkout/<str:order_id>/', views.checkout, name='checkout'),
    path('view/<str:order_id>/', views.order_detail, name='order-detail'),
]
