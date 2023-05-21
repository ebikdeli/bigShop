"""
There is no product list view. Our main product list view is in index page.
"""
from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView
from django.db import models

from .models import Product

from typing import Type, Any


class ProductListView(ListView):
    """For test purpose only"""
    model = Product
    queryset = Product.objects.all()
    template_name = 'shop/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """Every product has a detail view which customers can view product details and buy the product"""
    model: Type[models.Model] = Product
    template_name: str = 'shop/templates/shop/product_detail.html'
    context_object_name: str = 'product'
