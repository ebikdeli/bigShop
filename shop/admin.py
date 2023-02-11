from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Category, Brand, Device,\
                    Product, Color, ColorPrice


admin.site.register([Category, Brand, Device, Product, Color, ColorPrice])
