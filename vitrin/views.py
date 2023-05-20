from django.shortcuts import render


def index(request):
    """Index page of the shop"""
    return render(request, 'templates/index.html')
