from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Index page of the shop"""
    for k, v in request.headers.items():
        print(k, ' ===> ', v)
    return render(request, 'vitrin/templates/index.html')


def send_html(request):
    html = '<h1>This comes from server</h1><br><p>Should know it</p>'
    return HttpResponse(html)

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


# @csrf_exempt
def signup(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'user sign up data received', 'status': 200})


# @csrf_exempt
def signin(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'user sign in data received', 'status': 200})


# @csrf_exempt
def change_password(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'user password change data received', 'status': 200})


# @csrf_exempt
def edit_profile(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(data={'msg': 'user edit profile data received', 'status': 200})


# @csrf_exempt
def edit_profile_image(request):
    print(request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
        # Sended image(s) will be put in 'request.FILES'
        print(request.FILES)
        return JsonResponse(data={'msg': 'user edit profile image received', 'status': 200})
