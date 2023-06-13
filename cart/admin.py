from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin panel has changed"""
    list_display = ['user', 'price_pay', 'quantity', 'is_paid', 'is_active', 'updated']
    fields = ['user','session_key', ('price', 'price_pay', 'quantity'), ('is_paid', 'is_active'), 'slug', ('created', 'updated'), 'items']
    readonly_fields = ['session_key', 'created', 'updated', 'items', 'price', 'price_pay', 'quantity']
    
    @admin.display(boolean=False, description='cart items')
    def items(self, obj):
        """This field used to show all cart_items belong to this cart"""
        items = list()
        for item in obj.cart_item_cart.all():
            items.append(item.product.name)
        if not items:
            return 'No items in the cart'
        print(items)
        return items


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Changes for CartItem model"""
    list_display = ['cart', 'product', 'quantity', 'price', 'price_pay', 'updated']
    fields = ['cart', ('product', 'quantity'), ('price', 'price_pay'), ('created', 'updated')]
    readonly_fields = ['price', 'price_pay', 'created' ,'updated']
