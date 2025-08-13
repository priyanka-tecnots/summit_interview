from django.contrib import admin
from .models import Order, OrderItem, OrderStatus, ShippingAddress


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItem model.
    """
    model = OrderItem
    extra = 1
    readonly_fields = ['total_price']
    
    # fields = ['product', 'quantity', 'unit_price', 'total_price']


class OrderStatusInline(admin.TabularInline):
    """
    Inline admin for OrderStatus model.
    """
    model = OrderStatus
    extra = 0
    readonly_fields = ['created_at', 'created_by']
    
    # fields = ['status', 'notes', 'created_at', 'created_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin for Order model.
    """
    list_display = ['order_number', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer__username', 'customer__email']
    ordering = ['-created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    inlines = [OrderItemInline, OrderStatusInline]
    
    # list_editable = ['status']
    
    def get_customer_name(self, obj):
        return obj.customer.get_full_name()
    get_customer_name.short_description = 'Customer'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin for OrderItem model.
    """
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product__name']
    ordering = ['-created_at']
    readonly_fields = ['total_price', 'created_at']
    

    
    def get_order_number(self, obj):
        return obj.order.order_number
    get_order_number.short_description = 'Order Number'


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    """
    Admin for OrderStatus model.
    """
    list_display = ['order', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'created_by__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    

    
    def get_order_number(self, obj):
        return obj.order.order_number
    get_order_number.short_description = 'Order Number'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """
    Admin for ShippingAddress model.
    """
    list_display = ['user', 'address_line1', 'city', 'state', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['user__username', 'address_line1', 'city']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    

    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'User'
