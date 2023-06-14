from typing import Any
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

import constance

from .models import ContactUs, FAQ
from .forms import ContactUsModelForm


class FAQListView(ListView):
    """ListView to see all the FAQs"""
    model = FAQ
    queryset = FAQ.objects.all()
    template_name = 'support/faq-list.html'
    context_object_name = 'faqs'


class ContactUsCreateView(CreateView):
    """CreateView for users to create contact us"""
    model = ContactUs
    form_class = ContactUsModelForm
    template_name = 'support/contact-us-form.html'
    success_url = reverse_lazy('support:contact-thanks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_email'] = constance.config.email
        return context

    def get(self, request, *args, **kwargs):
        """Override this method to send user 'email' as intital data to the form."""
        user = self.request.user
        if user.is_authenticated:
            self.initial = {'name': user.phone} if user.phone else {'name': user.email}
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Because this method is the last method executed, we changed this method to add user (if existed) to
        newly created contact us object."""
        name = self.object.name
        name_query = Q(phone=name) | Q(email=name)
        user_qs = get_user_model().objects.filter(name_query).distinct()
        if user_qs.exists():
            self.object.user = user_qs.get()
            self.object.save()
        return super().get_success_url()


class ContactUsRedirectView(TemplateView):
    """TemplateView to show thanks message for user feedback in ContactUsCreateView"""
    template_name = 'support/contact-us-thanks.html'


class AboutUsView(TemplateView):
    """Template View to show 'About Us' page to users. It's content defined in 'constance' settings in 'base' module."""
    template_name = 'support/about-us.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['about_us'] = constance.config.about_us
    #     return context
