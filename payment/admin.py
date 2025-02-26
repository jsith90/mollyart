from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0
# Extend order model
class OrderAdmin(admin.ModelAdmin):
	model = Order
	readonly_fields = ['date_ordered']
	fields = ['full_name', 'email', 'shipping_address', 'amount_paid', 'date_ordered', 'shipped', 'date_shipped', 'invoice', 'payment_intent_id', 'paid', 'payer_id', 'payment_method']
	inlines = [OrderItemInline]
# unregister for inlines
admin.site.unregister(Order)
# reregister for inlines
admin.site.register(Order, OrderAdmin)