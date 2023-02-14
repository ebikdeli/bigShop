from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


def index(request):
    """Index page of the shop"""
    return render(request, 'vitrin/templates/index.html')
