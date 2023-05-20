from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import cache_page, never_cache
from cart.models import Cart
from .forms import UserLogin, UserSignUpForm, UserPasswordChangeForm
from .login import user_signup_login, user_password_change
from cart.cart_functions import synch_cart_session_cart_after_authentication


# @cache_page(60 * 15)
def classic_login(request):
    """Handles the classic or ordinary user login procedure"""
    if request.method == 'POST':
        login_form = UserLogin(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request,
                                username=request.POST['username_login'],
                                password=login_form.cleaned_data['password_login'])
            if user:
                login(request, user)
                # Synchronize Cart data with cart session data after login
                synch_cart_session_cart_after_authentication(Cart, request)
                return redirect(reverse('vitrin:index'))
            else:
                return redirect('login:login_signup')
    else:
        return redirect('login:login_signup')


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
        signup_form = UserSignUpForm(data=request.POST, files=request.FILES)
        if signup_form.is_valid():
            new_user = signup_form.save(commit=False)
            # Validate password manually (Django has odd behaviors to validate passwords) 
            if user_signup_login(request, new_user):
                # Synchronize Cart data with cart session data after login
                synch_cart_session_cart_after_authentication(Cart, request)
                # If user created successfully, direct him/her to his/her newly created profile
                return redirect('login:profile')
            # If there is a problem in 'user_signup_login' (eg: user could not login the website) redirect
            # the user to the main page
            return redirect('vitrin:index')
    # If any method used except for 'POST', redirect user to 'login_signup' view
    return redirect('login:login_signup')


@login_required
def change_password(request):
    """Handles changing of user password"""
    if request.method == 'POST':
        password_change_form = UserPasswordChangeForm(request.POST)
        # Form validation and other needed processes are implemented in 'user_password_change' function 
        if user_password_change(request, password_change_form):
            # If password change was a success, redirect user to the main page
            return redirect('login:profile')
        # If there is a problem in changing password in 'user_password_change' function, redirect user to this view again
        redirect('login:change_password')
    else:
        password_change_form = UserPasswordChangeForm()
    return render(request, 'login/templates/password_change.html', {'password_change_form': password_change_form})
