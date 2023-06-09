from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order
from .forms import OrderForm
from cart.models import Cart


@login_required
def order_form(request):
    """Before order created, the customer must fill a form to verify his/her address
    NOTE: user most be login"""
    # Get latest user 'address' and 'cart'
    address = request.user.address_user.first() if request.user.address_user.exists() else None
    cart = request.user.cart_user.first()
    if not cart:
        return redirect(reverse('vitrin:index'))
    if cart.quantity <= 1:
        return redirect(reverse('vitrin:index'))
    # ? Check if current 'cart' has any active order
    order_qs = cart.order_cart.filter(is_active=True, is_paid=False)
    if order_qs.exists():
        return redirect(reverse('vitrin:index'))
    # If method is POST process order-form and create a new Order for the user
    if request.method == 'POST':
        # We can also use 'cart_id' session to get current Cart
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
            order = cart.order_cart.create()
            # update 'user' and 'address'
            user = request.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.email = data['email']
            user.save()
            address.postal = data['postal']
            address.state = data['state']
            address.city = data['city']
            address.line = data['line']
            address.phone = user.phone
            address.save()
            return redirect(reverse('order:checkout', kwargs={'order_id': order.order_id}))
        else:
            print(order_form.errors)
    # When method is GET tell the user to fill 'order-form' before creation of order
    context = {'address': address}
    return render(request, 'order/order-form.html', context)


@login_required
def checkout(request, order_id=None):
    """Checkout page for the user order"""
    order = Order.objects.filter(order_id=order_id).get() if Order.objects.filter(order_id=order_id) else None
    if not order:
        print('THIS ORDER IS NOT REGISTERED')
        return reverse('vitrin:index')
    return render(request, 'order/checkout.html')


@login_required
def order_detail(request, order_id=None):
    """View details of the order"""
    order = Order.objects.filter(order_id=order_id).get() if Order.objects.filter(order_id=order_id) else None
    if not order:
        print('THIS ORDER IS NOT REGISTERED')
        return reverse('vitrin:index')
    return render(request, 'order/order-detail.html')
