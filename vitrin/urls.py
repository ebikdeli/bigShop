from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('ajax-response-test', views.ajax_response_test, name='ajax_response_test'),
    path('', views.index, name='index'),
]
