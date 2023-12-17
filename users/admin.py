from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import User
from .models import Address


class UserAdmin(AdminImageMixin, BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'first_name', 'last_name')}),
        ('Scores', {'fields': ('score', 'score_lifetime', 'discount_value', 'discount_percent')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Pictures', {'fields': ('picture',)}),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Address)
# If we don't unregister 'Group' we will get some Error if we want to reregister it with 'Permission'
admin.site.unregister(Group)
admin.site.register([Group, Permission])
