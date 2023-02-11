from django import forms

from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    """ModelForm for ContactUs model"""

    class Meta:
        model = ContactUs
        exclude = ['user']
