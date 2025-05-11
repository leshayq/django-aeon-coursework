from django.contrib import admin
from .models import ShippingAddress, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'full_name', 'total_price', 'status')
