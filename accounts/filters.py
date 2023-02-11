"""
https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html#integration-with-drf
"""
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

from .models import Address


class UserFilterSet(filters.FilterSet):
    """Filterset for User model"""

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'name', 'is_active',
                  'is_staff', 'is_admin', 'is_superuser',
                  'password']


class AddressFilterSet(filters.FilterSet):
    """Filterset for Address Model"""

    class Meta:
        model = Address
        fields = '__all__'
