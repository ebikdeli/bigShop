from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


def index(request):
    return render(request, 'vitrin/templates/index.html')


def ajax_response_test(request):
    # print(request.headers)
    # Test sending custom response headers
    request.META['NAME'] = 'EHSAN'
    data = {'msg': 'success', 'status': 'ok'}
    return JsonResponse(data=data, safe=False, headers={'NAME': 'EHSAN'})
