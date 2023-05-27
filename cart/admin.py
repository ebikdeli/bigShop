from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin panel has changed"""
    list_display = ['user', 'price', 'is_paid', 'is_active', 'updated']
    fields = ['user', 'price', 'session_key', ('is_paid', 'is_active'), 'slug', ('created', 'updated'),'items']
    readonly_fields = ['session_key', 'price', 'created', 'updated', 'items']
    
    @admin.display(boolean=False, description='cart items')
    def items(self, obj):
        """This field used to show all cart_items belong to this cart"""
        items = list()
        for items in obj.cart_item_cart.all():
            items.append(items)
        if not items:
            return 'No items in the cart'
        return items


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Changes for CartItem model"""
    list_display = ['cart', 'product', 'quantity', 'price', 'price_pay', 'updated']
    fields = ['cart', ('product', 'quantity'), ('price', 'price_pay'), ('created', 'updated')]
    readonly_fields = ['price', 'price_pay', 'created' ,'updated']
