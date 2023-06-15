# ! Data Validation should be happened in front-end
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import cache_page, never_cache
from cart.models import Cart
from .forms import UserPasswordChangeForm
from .login import user_signup_login, user_password_change
from cart.cart_functions import synch_cart_session_cart_after_authentication

import json


# @cache_page(60 * 15)
def classic_login(request):
    """Handles the classic or ordinary user login procedure"""
    if request.method == 'POST':
        data_json = request.POST['data']
        if not data_json:
            return JsonResponse(data={'msg': 'اطلاعاتی دریافت نشد', 'status': 'nok', 'code': 400})
        data = json.loads(data_json)
        user = authenticate(request,
                            username=data['username'],
                            password=data['password'])
        if user:
            login(request, user)
            # Synchronize Cart data with cart session data after login
            synch_cart_session_cart_after_authentication(Cart, request)
            return JsonResponse(data={'msg': 'ورود با موفقیت انجام گرفت', 'status': 'ok', 'code': 200})
        else:
            return JsonResponse(data={'msg': 'نام کاربری یا رمز عبور اشتباه است', 'status': 'nok','code': 401})
    else:
        return render(request, 'login/signin.html')


@login_required
def logout_view(request):
    """Logout user from website"""
    logout(request)
    messages.success(request, _('You have logout of your user account'))
    return redirect('vitrin:index')


# @cache_page(60 * 15)
def signup(request):
    """SignUp user after user proceeds with signup form in 'user_signup_view"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        data = json.loads(json_data)
        new_user = get_user_model().objects.filter(username=data['username'])
        if new_user.exists():
            return JsonResponse(data={'msg': f'کاربر {data["username"]} در حال حاضر وجود دارد', 'status': 'nok', 'code': 400})
        new_user = get_user_model()(username=data['username'], password=data['password'])
        if user_signup_login(request, new_user):
            # Synchronize Cart data with cart session data after login
            synch_cart_session_cart_after_authentication(Cart, request)
            # If user created successfully, direct him/her to his/her newly created profile
            return JsonResponse(data={'msg': f"کاربر جدید ساخته شد", 'status': 'ok', 'code': 201})
        # If there is a problem in 'user_signup_login' (eg: user could not login the website) redirect
        # the user to the main page
        return JsonResponse(data={'msg': 'کاربر جدید ایجاد شد اما لاگین انجام نشد', 'status': 'nok', 'code': 301})
    # If any method used except for 'POST', redirect user to 'login_signup' view
    else:
        return render(request, 'login/signup.html')


@login_required
def password_change(request):
    """Handles changing of user password"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 400})
        data = json.loads(json_data)
        user = authenticate(request, username=request.user.username, password=data['password'])
        if not user:
            return JsonResponse(data={'msg': 'رمز عبور اشتباه است', 'status': 'nok', 'code': 402})
        # If current password is valid, change user password with new-password
        user.password = make_password(data['new-password'])
        # user.save()
        return JsonResponse(data={'msg': 'رمز عبور با موفقیت تغییر داده شد', 'status': 'ok', 'code': 200})
    # Any request method except for the 'POST" resulted in following error
    else:
        return JsonResponse(data={'msg': 'متد درخواستی اشتباه است', 'status': 'nok', 'code': 401})


@login_required
def edit_profile(request):
    """Edit user profile from dashboard"""

    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        data = json.loads(json_data)
        fields_number = 0
        # Check if address data changed
        address = request.user.address_user.first()
        try:
            if data['address'] != address.line:
                address.line = data['address']
                address.save()
                fields_number += 1
                data.pop('address')
        except KeyError:
            pass
        # Check if user data changed
        user = get_user_model().objects.get(id=request.user.id)
        # ? Instead fo below for block, we can use this line: "request.user.__dict__.update(**data)"
        for k, new_value in data.items():
            for field, old_value in user.__dict__.items():
                if k == field:
                    print(field, ' ===> ', old_value)
                    print(field, ' ===> ', new_value)
                    fields_number += 1
                    user.__dict__[field] = new_value
        if fields_number:
            user.save()
            return JsonResponse(data={'msg': 'اطلاعات شما با موفقیت تغییر کرد', 'status': 'ok', 'code': 200})
        # If there are no fields to change, return below message
        return JsonResponse(data={'msg': 'فیلدی برای تغییر کردن وجود نداشت', 'status': 'nok', 'code': 402})
    # If any method requested except for POST returns following response
    return JsonResponse(data={'msg': 'متد اشتباهی ارسال شده', 'status': 'nok', 'code': 400})


@login_required
def edit_profile_image(request):
    """Edit user profile image in user dashboard"""
    if request.method == 'POST':
        files = request.FILES
        if not files:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        request.user.picture = files['image']
        request.user.save()
        return JsonResponse(data={'msg': 'تصویر با موفقیت تغییر پیدا کرد', 'status': 'ok', 'code': 200})
    else:
        return JsonResponse(data={'msg': 'متد اشتباهی ارسال شده', 'status': 'nok', 'code': 400})
