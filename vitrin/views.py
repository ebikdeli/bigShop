from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Index page of the shop"""
    return render(request, 'vitrin/templates/index.html')


# * These hooks will be used to test against api hooks
# @csrf_exempt
def pr_data(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'OK', 'status': 200})


# @csrf_exempt
def add_product_cart(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'product added to cart', 'status': 200})


# @csrf_exempt
def delete_product_cart(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'product deleted from the cart', 'status': 200})


# @csrf_exempt
def change_product_quantity_cart(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'product quantity changed', 'status': 200})
