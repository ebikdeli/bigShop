from django.contrib import admin

from .models import Order, OrderItem, Shipment


admin.site.register([Order, OrderItem])


@admin.register(Shipment)
class OrderAdmin(admin.ModelAdmin):
    fields = ['shipment_id', 'user', 'address', 'order', 'cost', 'is_send', 'slug']
    readonly_fields = ['shipment_id', 'slug']
    list_display = ['shipment_id', 'user', 'cost', 'is_send']
    list_editable = ['cost', 'is_send']
    list_display_links = ['shipment_id', 'user']
