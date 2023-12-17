"""
https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
"""
from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'accounts'

router = routers.DefaultRouter()

router.register('user', views.UserViewSet, 'user')
router.register('address', views.AddressViewSet, 'address')

urlpatterns = [
    path('', include(router.urls)),
]
