from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Q

import re


def validate_password(request, password):
    """Django has problem with custom User password validation so we have to make password validation in main view.
    It must be sofesticated password validation"""
    if len(password) < 4:
        messages.error(request, _('Password must be atleast 4 characters'))
        # messages.error(request, _('طول رمز عبور کمتر از 4 کاراکتر است'))
        return False
    if len(password) > 20:
        messages.error(request, _('Password is too long'))
        # messages.error(request, _('طول رمز عبور از حد مجاز بیشتر است'))
        return False

    return True


class UserLogin(forms.Form):
    """Simple form for ordinary users to login from 'login' app."""
    username_login = forms.CharField()
    password_login = forms.CharField(widget=forms.PasswordInput)


class UserSignUpForm(forms.ModelForm):
    """ModelForm for ordinary users to signup from 'login' app."""
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text=_('Password must be atleast four characters'))
                               # help_text=_('رمز عبور باید بیش از 6 کاراکتر باشد'))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'confirm_password']
        """
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password',
                  'address', 'phone', 'picture']
        """
        widgets = {
            'username': forms.TextInput,
            'password': forms.PasswordInput(attrs={'required': False}),  # <==> This is wrong. 'required is a option
        }
        error_messages = {
            'username': {'unique': 'This username already in use'},
            # 'username': {'unique': 'این نام کاربری قبلا استفاده شده'},
            'email': {'unique': 'This email is already registered'},
            # 'email': {'unique': 'این ایمبل قبلا استفاده شده'},
            'password': {'required': 'please enter password'}
            # 'password': {'required': 'لطفا رمز عبور را وارد کنید'}
        }

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('Passwords are not match')
        return data
    
    def clean(self):
        """Check if username is match to an 'email' or 'phone'"""
        username = self.cleaned_data['username']
        # Check if received username is a valid email or phone number
        regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        regex_phone =  re.compile(r'09[0-3][0-9]-?[0-9]{3}-?[0-9]{4}')
        if not (re.fullmatch(regex_email, username) or re.fullmatch(regex_phone, username)):
            raise forms.ValidationError(_('Username is not valid email or phone number'))
        # Check if received username is already registered email or phone number for another user
        qs = get_user_model().objects.filter(Q(phone=username) | Q(email=username))
        if qs.exists():
            raise forms.ValidationError(message=_('THIS USERNAME CAN NOT BE TAKEN'))
        return super().clean()


class UserAccountChangeForm(forms.Form):
    """Form for users to change and edit their account information from 'login' app"""
    # 'id' used for query the current user
    id = forms.CharField(required=True, widget=forms.HiddenInput())
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False,
                            validators=[
                                        MaxLengthValidator(14, _("To long phone number")),
                                        MinLengthValidator(10, _("To short phone number"))
                                        ])
    picture = forms.ImageField(required=False)

    def clean_username(self):
        """If there are email or phone exist with requested username and raise validation error if exist"""
        id = self.cleaned_data['id']
        username = self.cleaned_data['username']
        # Two following lines do the same thing
        # qs = get_user_model().objects.exclude(id=id).filter((Q(phone=username) | Q(email=username)))
        qs = get_user_model().objects.filter((~Q(id=id))& (Q(phone=username) | Q(email=username)))
        if qs.exists():
            raise forms.ValidationError(message=_(f"'{username}' already exists and could not be taken"))
        return username


class UserAddressChangeForm(forms.Form):
    """To change and edit user address data from profile"""
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    line = forms.CharField(required=False)
    code = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    postal = forms.CharField(required=False)


class UserPasswordChangeForm(forms.Form):
    """Form for ordinary users to change their password from 'login' app."""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Current password')}),)
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('رمز عبور')}),)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Enter new password')}),
                                   help_text=_('Password must atleast be 4 characters'))
    # new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('رمز عبور جدید')}),
                                   # help_text=_('رمز عبور جدید باید حداقل 6 کاراکتر داشته باشد'))
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password')}))
    # new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('تکرار رمز عبور جدید')}))
    
    def clean_new_password_confirm(self):
        data = self.cleaned_data
        if data['new_password'] != data['new_password_confirm']:
            raise forms.ValidationError(_('Password mismatch'))
            # raise forms.ValidationError(_('تکرار رمز عبور جدید را به درستی وارد کنید'))
        return data
