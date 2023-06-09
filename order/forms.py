from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)
    postal = forms.CharField(required=True)
    state = forms.CharField(required=True)
    city = forms.CharField(required=True)
    line = forms.CharField(required=True)
