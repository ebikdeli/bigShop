"""
** If any CartItem instance created or updated, its Cart 'total_quantity', 'price', and 'price_end' fields updated
automatically.
** CartItem 'price' and 'price_end' calculated automatically based on 'quantity' field and 'product' foreign key.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Sum


@receiver(pre_save, sender='cart.CartItem')
def calculate_cart_item_price_and_price_end_based_quantity(sender, instance=None, **kwargs):
    """Calculate 'price' and 'price_end' fields based on 'quantity' field"""
    if (instance.quantity and not instance.price) or instance._quantity != instance.quantity:
        instance.price = instance.quantity * instance.product.price
        instance.price_end = instance.quantity * instance.product.price_end


@receiver(post_save, sender='cart.CartItem')
def calculate_cart_total_quantity_and_price_and_price_end(sender, created=None, instance=None, **kwargs):
    """Calculate cart 'total_quantity' and 'price' and 'end_price' fields based on the current 'cart.cartitem_cart'
    reverse relation field"""
    cart = instance.cart
    # Calculate 'total_quantity' field
    updatedCartTotalQuantity = cart.cartitem_cart.all().aggregate(new_quantity=Sum('quantity'))
    cart.total_quantity = updatedCartTotalQuantity['new_quantity']
    # Calculate 'price' field
    updatedCartPrice = cart.cartitem_cart.all().aggregate(new_price=Sum('price'))
    cart.price = updatedCartPrice['new_price']
    # Calculate 'price_end' field
    updatedCartPriceEnd = cart.cartitem_cart.all().aggregate(new_price_end=Sum('price_end'))
    cart.price_end = updatedCartPriceEnd['new_price_end']
    # save cart to update its db
    instance.cart.save()
