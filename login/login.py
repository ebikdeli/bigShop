"""
This module contains functions to handle login and signup procedure and used in 'login.views' module.
These functions defined for better code management and code modularity.
"""
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


def user_signup_login(request, user):
    """
    Login user with session mode after which he/she signup to the website. Note that because we use more
    than one (default) login backend, we must set backend the one we want. If we don't this we receive errors.
    """
    try:
        user.set_password(user.password)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, _('Welcome to Green Apple'))
        # messages.success(request, _('به وبسایت گرین اپل خوش آمدید'))
        return True
    except KeyboardInterrupt:
        messages.error(request, _('There is a problem in login the new user. Please try later'))
        return False


def user_password_change(request, form):
    """Handle user password change form"""
    if form.is_valid():
        user = request.user
        # First we must test user authentication with the password to know if there is a user with the entered password
        # in db. Note that we do this when currently user is authenticated!
        if authenticate(request, username=user.username, password=form.cleaned_data['password']):
            # If user authenticated with current password and new password validated in 'validate_password' implement
            # the password change
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            # login user after changing the password
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return True
    # If the whole form validation failed, returns None
    return None


def user_change_validation_check_cleaner(request, form):
    """
    NOTE: 'username' does not needed here because username field validated before FORM.is_valid() method.
    """
    error = 0
    # Just get needed fields for every users except for current user. Remember 'values' returns a list of dictionary
    users_except_current_list = get_user_model().objects.exclude(id=request.user.id).values('username', 'email', 'phone')
    # List of fields we want to search in form.changed_data
    important_fields_list = ['username', 'email', 'phone']
    for field in form.changed_data:
        if field in important_fields_list:
            field_value = form.cleaned_data[field]
            for user_dict in users_except_current_list:
                if field_value in user_dict.values():
                    messages.error(request, _(f"This {field} is already register"))
                    error += 1
    return error


def change_user_account_data(request, user, form):
    """Change user account based on user account change form"""
    try:
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.phone = form.cleaned_data['phone']
        user.picture = form.cleaned_data['picture']
        user.save()
        messages.success(request, _('Changes implemented successfully'))
        # messages.success(request, _('تغییرات با موفقیت اعمال شد'))
        return True
    except KeyError:
        messages.error(request, _('Problem occured, no changes implemented'))
        # messages.error(request, _('مشکل پیش آمده. تغییرات اعمال نشد'))
        return None


def change_user_address_data(request, address, form):
    """Change user address based on user address change form"""
    try:
        address.state = form.cleaned_data['state']
        address.city = form.cleaned_data['city']
        address.line = form.cleaned_data['line']
        address.code = form.cleaned_data['code']
        address.phone = form.cleaned_data['phone']
        address.postal = form.cleaned_data['postal']
        address.save()
        messages.success(request, _('Changes implemented for address successfully'))
        return True
    except KeyError:
        messages.error(request, _('Problem occured, no changes implemented for address'))
        return None
