from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Q


class UserAccountChangeForm(forms.Form):
    """Form for users to change and edit their account information from 'login' app"""
    # 'id' used for query the current user
    id = forms.CharField(required=True, widget=forms.HiddenInput())
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
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
