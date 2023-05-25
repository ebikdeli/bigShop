"""
There is no product list view. Our main product list view is in index page.
"""
from django.views.generic import DetailView
from django.db import models

from .models import Product
from typing import Type


class ProductDetailView(DetailView):
    """Every product has a detail view which customers can view product details and buy the product"""
    model: Type[models.Model] = Product
    template_name: str = 'product/product-detail.html'
    context_object_name: str = 'product'
