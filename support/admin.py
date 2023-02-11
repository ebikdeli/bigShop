from django.contrib import admin

from .models import ContactUs, FAQ


admin.site.register({ContactUs, FAQ})
