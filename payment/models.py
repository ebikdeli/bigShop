from django.db import models
from django.db.models import QuerySet
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from _resources.func import get_random_string
import uuid

class Payment(models.Model):
    """Everytime a payment is to be made, a model is created"""
    PGI_CHOICES = [
        ('zarrin', 'zarrin'),
        ('idpay', 'idpay'),
    ]
    payment_id = models.CharField(verbose_name=_('payment_id'), max_length=40, default=uuid.uuid4, editable=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            verbose_name=_('user'),
                            related_name='payment_user',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True)
    order = models.ForeignKey('order.Order',
                            verbose_name=_('order'),
                            related_name='payment_order',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0)
    describtion = models.TextField(verbose_name=_('describtion'), blank=True)
    pgi = models.CharField(verbose_name=_('gateway interface (pgi)'), choices=PGI_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self) -> str:
        return f'{self.payment_id}'
    
    def cart(self) -> object|None:
        """Get the cart for this payment"""
        if self.order:
            return self.order.cart
        return None

    def order_items(self) -> object|None:
        """Get order items of the payment"""
        if self.order:
            return self.order.order_item_order.all()
        return None
    
    def products(self) -> list:
        """Get products of the payment order"""
        products = list()
        products.extra
        if self.order:
            for oi in self.order.order_item_order.all():
                products.append(oi.product)
        return products
