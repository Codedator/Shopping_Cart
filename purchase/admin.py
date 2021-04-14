from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingDetail)
admin.site.register(FinalDiscount)
