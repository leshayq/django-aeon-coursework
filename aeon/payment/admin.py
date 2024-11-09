from django.contrib import admin
from .models import ShippingAddress, Order

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'number', 'city', 'street_address', 'department')
    ordering = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'formatted_shipping_address', 'total', 'status', 'delivery_type', 'created', 'updated', 'paid')
    ordering = ('-created',)

    def formatted_shipping_address(self, obj):
        if obj.shipping_address:
            return (
                f"ПІБ: {obj.shipping_address.full_name}\n"
                f"Пошта: {obj.shipping_address.email}\n"
                f"номер телефону: {obj.shipping_address.number}\n"
                f"Місто: {obj.shipping_address.city}\n"
                f"Адреса: {obj.shipping_address.street_address}\n"
                f"Відділення: {obj.shipping_address.department}"
            )
        return '-'
    formatted_shipping_address.short_description = 'Доставка'
    formatted_shipping_address.admin_order_field = 'Доставка'

