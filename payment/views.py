from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from order.models import Order


@login_required
def payment_request(request, order_id=None):
    """Payment request for user to pay for the order"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    context = {'order': order}
    return render(request, 'payment/payment-request.html', context=context)


@login_required
def zarrin_pal_request(request, order_id=None):
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    """If user select zarrin-pal pgi redirected here"""
    return JsonResponse(data={'msg': 'درگاه زرین پال انتخاب شده', 'order-id': order.order_id})


@login_required
def next_pay_request(request, order_id=None):
    """If user select next-pay pgi redirected here"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    return JsonResponse(data={'msg': 'درگاه نکست پی انتخاب شده', 'order-id': order.order_id})
