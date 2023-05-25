from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from .models import Cart
import json


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


def add_product_cart(request):
    """Add item to cart"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'status': 401})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        color_name = data.get('color', None)
        quantity = data.get('quantity', None)
        if not product_id:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'status': 206})
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'محصولی با مشخصه ارسالی یافت نشد', 'status': 205})
        # * Put product into the cart
        product = product_qs.get()
        if color_name:
            color = Color.objects.filter(name=color_name)
            
            
    # If any method except of the 'POST' come, send following message
    return JsonResponse(data={'msg': 'bad request method', 'status': 402})
