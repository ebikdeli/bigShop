from django.db.models.signals import post_init
from django.dispatch import receiver


@receiver(post_init, sender='cart.Cart')
def calculate_cart_cart_item_orders(sender, instance=None, *args, **kwargs):
    """Check if cart has any order_item but do not have them as cart_item then create them"""
    if not instance.price and not instance.price_pay:
        if instance.order_cart.first():
            if instance.order_cart.first().quantity_total and instance.order_cart.first().price:
                if not instance.is_paid and instance.order_cart.first().is_paid:
                    instance.is_paid = True
                for order_item in instance.order_cart.first().order_item_order.all():
                    instance.cart_item_cart.create(
                        product=order_item.product,
                        quantity=order_item.quantity,
                        price=order_item.price,
                        price_pay=order_item.price_pay
                    )
                instance.save()
