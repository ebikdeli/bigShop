from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# This variable won't deleted untill server restart again
COOKIES = []

# if CONTENT_TYPE == 'text/plain'
    # This is for full stack


def index(request):
    """Index page of the shop"""
    print(request.META.get('HTTP_ACCEPT'))
    return render(request, 'vitrin/templates/index.html')


from django import forms
class AjaxForm(forms.Form):
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    name = forms.CharField(required=False)
    password = forms.CharField(required=False)


def ajax_response_test(request):
    """
    Test varoud part of an ajax request and the data client sends to server and received by it. We have created a
    form to bound received data to the Form object to easily clean received data by it.
    """
    if request.method == 'POST':
        # data = request.POST
        # print(request.POST)
        # for k, v in request.POST.items():
        #     print(k, ' ===> ', v)
        form = AjaxForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    # for header, value in request.headers.items():
    #     print(header, ' ===> ', value)
    #     if header == 'Cookie':
    #         COOKIES.append(value)
    # Test sending custom response headers
    request.META['NAME'] = 'EHSAN'
    data = {'msg': 'success', 'status': 'ok'}
    print(request.META.get('HTTP_ACCEPT'))
    return JsonResponse(data=data, safe=False, headers={'NAME': 'EHSAN'})
