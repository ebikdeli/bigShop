from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    email = forms.CharField()
    postal = forms.CharField()
    state = forms.CharField()
    city = forms.CharField()
    line = forms.CharField()
