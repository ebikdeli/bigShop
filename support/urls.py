from django.urls import path

from . import views


app_name = 'support'

urlpatterns = [
    path('faq/', views.FAQListView.as_view(), name='faq-list'),
    path('contact/', views.ContactUsCreateView.as_view(), name='contact-form'),
    path('contact-thanks/', views.ContactUsRedirectView.as_view(), name='contact-thanks'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
]
