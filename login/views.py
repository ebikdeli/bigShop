from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import cache_page, never_cache
from cart.models import Cart
from .forms import UserLogin, UserSignUpForm, UserAccountChangeForm, UserAddressChangeForm, UserPasswordChangeForm
from .forms import validate_password
from .login import user_change_validation_check_cleaner, user_signup_login,change_user_account_data,\
                   change_user_address_data, user_password_change
from cart.cart_functions import synch_cart_session_cart_after_authentication


# @cache_page(60 * 10)
def login_signup(request):
    """Render forms and templates for user to login or signup to the site"""
    if request.method == 'GET':
        login_form = UserLogin()
        signup_form = UserSignUpForm()
        context = {'login_form': login_form, 'signup_form': signup_form}
        return render(request, 'login/templates/login_signup.html', context)
    else:
        return redirect('login:login_signup')


# @cache_page(60 * 15)
def classic_login(request):
    """Handles the classic or ordinary user login procedure"""
    if request.method == 'POST':
        login_form = UserLogin(data=request.POST)

        if login_form.is_valid():
            user = authenticate(request, username=request.POST['username_login'],
                                password=login_form.cleaned_data['password_login'])
            if user:
                login(request, user)
                # Synchronize Cart data with cart session data after login
                synch_cart_session_cart_after_authentication(Cart, request)
                messages.add_message(request, messages.SUCCESS, _('Successfully login'))
                # messages.add_message(request, messages.SUCCESS, _('با موفقیت وارد حساب کاربری خود شدید'))
                return redirect(reverse('vitrin:index'))
            else:
                messages.warning(request, _('username or password is incorrect'))
                # messages.add_message(request, messages.SUCCESS, _('با موفقیت وارد حساب کاربری خود شدید'))
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
            if validate_password(request, new_user.password):
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


# @cache_page(60 * 10)
@login_required
def profile(request):
    """Setup to view user profile and change user account data and user address"""
    # 'account_data' dict used to initialized form for the 'UserAccountChangeForm' form in the view
    user = request.user
    account_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'picture': user.picture
    }
    # Initializing user address
    address = user.address
    address_data = dict()
    if address:
        address_data = {
            'id': address.id,
            'state': address.state,
            'city': address.city,
            'line': address.line,
            'code': address.code,
            'phone': address.phone,
            'postal': address.postal,
        }
    # Setup forms
    user_account_change_form = UserAccountChangeForm(initial=account_data)
    user_address_change_form = UserAddressChangeForm(initial=address_data)
    # If we want to setup form in the template with ordinary html tags, we must sent 'data' dict to setup initializations
    context = {'user_account_change_form': user_account_change_form,
               'account_data': account_data,
               'user_address_change_form': user_address_change_form,
               'address_data': address_data,
               }
    return render(request, 'login/templates/profile.html', context)


@login_required
def profile_change_user_account(request):
    """Change user accounts"""
    if request.method == 'POST':
        user = request.user
        account_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'picture': user.picture
    }
        user_account_change_form = UserAccountChangeForm(data=request.POST, files=request.FILES, initial=account_data)
        if user_account_change_form.is_valid():
            # If user changes their profile, do the following
            if user_account_change_form.has_changed():
                errors = user_change_validation_check_cleaner(request, user_account_change_form)
                if not errors:
                    # If no error received, proceeds with implementing the change to user profile
                    change_user_account_data(request, user, user_account_change_form)
            else:
                messages.info(request, _('No change received'))
    # Whether changes implemented or not, or even request method anything except as 'POST' redirect user to 'profile'
    # view with some messages
    return redirect('login:profile')


@login_required
def profile_change_user_address(request):
    """Change user location"""
    if request.method == 'POST':
        address = request.user.address
        address_data = {
            'id': address.id,
            'state': address.state,
            'city': address.city,
            'line': address.line,
            'code': address.code,
            'phone': address.phone,
            'postal': address.postal,
        }
        user_address_change_form = UserAddressChangeForm(data=request.POST, initial=address_data)
        if user_address_change_form.is_valid():
            if user_address_change_form.has_changed():
                # If there is any change in the address form, proceeds to implement changes
                change_user_address_data(request, address, user_address_change_form)
            else:
                # If no changes received, put that in the message
                messages.info(request, _('No change received for user address'))
    # Whether changes implemented or not, or even request method anything except as 'POST' redirect user to 'profile'
    # view with some messages
    return redirect('login:profile')
