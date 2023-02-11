from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Cart


def cart_view(request):
    return render(request, 'cart/templates/cart/cart_view.html')


def append_product_to_cart(request):
    """Add product to session by 'product_id' and 'product.id' form fields."""
    if request.method == 'POST':
        # Process received Data from the 'product_detail' or 'cart_view' views
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        Cart.objects.append_item(quantity, request.session['cart_id'], request, product_id)
        return redirect('cart:cart_view')


def change_cartitem_quantity(request):
    """Change quantity of the CartItem in the cart either by 'CartItem.id' or 'Product.product_id'."""
    cartitem_id = request.GET.get('cartitem_id')
    quantity = request.GET.get('quantity')
    cart = Cart.objects.get(id=request.session['cart_id'])
    Cart.objects.change_item_quantity(quantity, cart.id, request, cartitem_id)
    return redirect('cart:cart_view')


def delete_product_from_cart(request):
    """Delete a product from session by 'CartItem.id' or 'product_id' form field"""
    cartitem_id = request.GET.get('cartitem_id')
    cart = Cart.objects.get(id=request.session['cart_id'])
    Cart.objects.delete_item(cart.id, request, cartitem_id)
    return redirect('cart:cart_view')


def clean_cart(request):
    """Clean all items from the Cart and reset sessions"""
    Cart.objects.clean(request.session['cart_id'], request)
    return redirect('cart:cart_view')
 