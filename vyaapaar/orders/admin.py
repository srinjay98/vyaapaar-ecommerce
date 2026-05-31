from django.contrib import admin

# Register your models here.

from .models import (
    Order,
    OrderItem,
    Payment,
    Coupon
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Coupon)