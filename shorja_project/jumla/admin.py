from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Governorate)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Bill)
admin.site.register(User)
