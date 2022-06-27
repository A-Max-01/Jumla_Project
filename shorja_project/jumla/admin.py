from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import *


class MyAdminSite(admin.AdminSite):
    site_header = 'Monty Python administration'


admin.site.site_header = 'الشورجة بين ايدك'


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups',)}),
        # (('Important dates'), {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)


admin_site = MyAdminSite(name='myadmin')


admin.site.register(Category)
admin.site.register(Governorate)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(product_Images)
# admin.site.register(Cart)
# admin.site.register(Bill)
admin.site.register(User, CustomUserAdmin)
