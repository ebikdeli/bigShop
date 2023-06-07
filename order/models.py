from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from product.models import ColorPrice
from _resources import func


class Order(models.Model):
    """Represents every Order customers register"""
    order_id = models.CharField(verbose_name=_('order_id'), max_length=10, unique=True, editable=False)
    cart = models.ForeignKey('cart.Cart',
                            verbose_name=_('cart'),
                            on_delete=models.CASCADE,
                            related_name='order_cart',
                            blank=True,
                            null=True)
    discounts = models.DecimalField(verbose_name=_('discounts'), max_digits=8, decimal_places=0, default=0)
    is_paid = models.BooleanField(verbose_name=_('is_paid'), default=False)
    is_received = models.BooleanField(verbose_name=_('has_received'), default=False)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-updated']
    
    def __str__(self):
        return f'{self.order_id}'
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Create order_id field
        if not self.order_id:
            self.order_id = func.get_random_string(10)
        # Create slug field
        if not self.slug:
            self.slug = slugify(self.order_id)
    
    @property
    def user(self):
        """Get order user"""
        return self.cart.user
    
    @property
    def price(self):
        """Get order price from order_items of current order"""
        price = 0
        if self.order_item_order.exists():
            for order_item in self.order_item_order.all():
                price += int(order_item.price * order_item.quantity)
        return price
    
    @property
    def price_pay(self):
        """Get order price_pay from order_items of current order"""
        price_pay = 0
        if self.order_item_order.exists():
            for order_item in self.order_item_order.all():
                price_pay += int(order_item.price_pay * order_item.quantity)
        price_pay -= self.discounts
        return price_pay if price_pay > 0 else 0
    
    @property
    def quantity_total(self):
        """Get quantity of the items of current order"""
        quantity_total = 0
        if self.order_item_order.exists():
            for order_item in self.order_item_order.all():
                quantity_total += order_item.quantity
        return quantity_total



class OrderItem(models.Model):
    """Represents every item user orders"""
    order = models.ForeignKey('Order',
                            verbose_name=_('order'),
                            related_name='order_item_order',
                            on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',
                                verbose_name=_('order_item_product'),
                                related_name='order_item_product',
                                on_delete=models.CASCADE)
    color = models.ForeignKey('product.Color',
                            verbose_name=_('color'),
                            related_name='order_item_color',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
        ordering = ['-updated']
    
    def __str__(self) -> str:
        return f'{self.order.order_id}: {self.product.name}'
    
    @property    
    def user(self):
        """Get OrderItem user"""
        self.order.cart.user
    
    @property
    def price(self):
        """Get price of the orderitem"""
        price = self.quantity * self.product.price
        cp = ColorPrice.objects.filter(product=self.product, color=self.color)
        if cp.exists():
            price += (cp.get().extra_price * self.quantity)
        return price
    
    @property
    def price_pay(self):
        """Get price_pay of the orderitem by effecting the product discount and posible color price gap"""
        # price_pay = self.quantity * (self.product.price - self.product.discount)
        price_pay = self.price() - (self.product.discount * self.product.quantity)
        if self.color:
            cp = ColorPrice.objects.filter(product=self.product, color=self.color)
            if cp.exists():
                price_pay += cp.get().extra_price
        return price_pay
