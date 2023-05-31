from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from .models import Cart
from product.models import Product, Color
import json


def cart_view(request):
    # Following if block used to test how data received from client shown in backend
    # if request.method == 'POST':
    #     print(request.POST)
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
        # * Process received data and check if there is no error
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        color_name = data.get('color', None)
        quantity = data.get('quantity', None)
        if not product_id:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'محصولی با مشخصه ارسالی یافت نشد', 'code': 402, 'status': 'nok'})
        # * Put product into the cart
        if request.user.is_authenticated:
            cart_id = request.user.cart_user.first().id
        else:
            try:
                cart_id = request.session['cart_id']
            except KeyError:
                return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'ارتباط با سبد خرید برقرار نشد', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        product = product_qs.get()
        result = cart.append_item(request, quantity, product_id, color_name)
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و محصول در سبد خرید ثبت نشد', 'code': 402, 'status': 'nok'})
        # Item successfully added to cart
        return JsonResponse(data={'msg': 'محصول در سبد خرید قرار گرفت', 'code': 201, 'status': 'ok'})
    # If any method except of the 'POST' come, send following message
    return JsonResponse(data={'msg': 'bad request method', 'code': 400, 'status': 'nok'})


def change_product_cart(request):
    """Change number of items in the cart"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        cart_id = data.get('cart-id', None)
        quantity = data.get('quantity', None)
        if not product_id:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'محصولی با مشخصه ارسالی یافت نشد', 'code': 402, 'status': 'nok'})
        # * Put product into the cart
        if not cart_id:
            return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'ارتباط با سبد خرید برقرار نشد', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        product = product_qs.get()
        # Get current CartItem
        cart_item_qs = cart.cart_item_cart.filter(product=product)
        if not cart_item_qs.exists():
            return JsonResponse({'msg': 'آیتم مورد نظر پیدا نشد', 'code': 402, 'status': 'nok'})
        cart_item = cart_item_qs.get()
        result = cart.change_item_quantity(quantity, request, cart_item)
        if not result:
            return JsonResponse(data={'msg': 'عملیات تغییر محصول با مشکل مواجه شد', 'code': 402, 'status': 'nok'})
        # If there is no error in the request return success message
        return JsonResponse(data={'msg': 'تغییر تعداد محصول با موفقیت انجام شد', 'code': 201, 'status': 'ok'})
    # If any method called except for POST, return following code
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})


def delete_item_cart(request):
    """"Delete selected item from the cart"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        cart_id = data.get('cart-id', None)
    
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})
