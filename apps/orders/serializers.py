from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus, ShippingAddress


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_name', 'product_price',
            'quantity', 'unit_price', 'total_price', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total_price']
    



class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderStatus model.
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = OrderStatus
        fields = [
            'id', 'order', 'status', 'status_display', 'notes',
            'created_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']


class ShippingAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for ShippingAddress model.
    """
    class Meta:
        model = ShippingAddress
        fields = [
            'id', 'user', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'phone', 'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    



class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'status', 'status_display',
            'shipping_address', 'billing_address', 'subtotal', 'tax_amount',
            'shipping_cost', 'total_amount', 'notes', 'created_at', 'updated_at',
            'items', 'status_history'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']
    



class OrderListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for order listing.
    """
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'status', 'status_display',
            'total_amount', 'created_at', 'items_count'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'items_count']
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for order creation.
    """
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'customer', 'shipping_address', 'billing_address',
            'subtotal', 'tax_amount', 'shipping_cost', 'notes', 'items'
        ]
    



class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating order status.
    """
    class Meta:
        model = Order
        fields = ['status', 'notes']
    

