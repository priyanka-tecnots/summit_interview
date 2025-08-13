from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Sum, Count
from django_filters import rest_framework as filters

from .models import Order, OrderItem, OrderStatus, ShippingAddress
from .serializers import (
    OrderSerializer, OrderListSerializer, OrderCreateSerializer,
    OrderItemSerializer, OrderStatusSerializer, ShippingAddressSerializer,
    OrderUpdateStatusSerializer
)


class OrderFilter(filters.FilterSet):
    """
    Filter for Order model.
    """
    search = filters.CharFilter(method='search_filter')
    min_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    customer = filters.NumberFilter(field_name='customer__id')
    status = filters.CharFilter(field_name='status')
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = ['search', 'min_amount', 'max_amount', 'customer', 'status', 'date_from', 'date_to']
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(order_number__icontains=value) |
            Q(customer__username__icontains=value) |
            Q(customer__email__icontains=value)
        )


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order model.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = OrderFilter
    search_fields = ['order_number', 'customer__username', 'customer__email']
    ordering_fields = ['order_number', 'total_amount', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderUpdateStatusSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset
        return queryset.select_related('customer').prefetch_related('items', 'status_history')
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def pending_orders(self, request):
        """
        Get all pending orders.
        """
        orders = Order.objects.all()
        pending_orders = [order for order in orders if order.status == 'pending']
        
        serializer = OrderListSerializer(pending_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update order status.
        """
        order = self.get_object()
        serializer = OrderUpdateStatusSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            old_status = order.status
            serializer.save()
            
           
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def completed_orders(self, request):
        """
        Get all completed orders.
        """
        completed_orders = Order.objects.filter(status='delivered')
        serializer = OrderListSerializer(completed_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        """
        Cancel an order.
        """
        order = self.get_object()
        
        # if order.status not in ['pending', 'confirmed']:
        #     return Response(
        #         {'error': 'Order cannot be cancelled in current status'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        order.status = 'cancelled'
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderItem model.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().select_related('order', 'product')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # product = serializer.validated_data['product']
            # if product.stock_quantity < serializer.validated_data['quantity']:
            #     return Response(
            #         {'error': 'Insufficient stock'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderStatus model.
    """
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().select_related('order', 'created_by')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # order = serializer.validated_data['order']
            # status = serializer.validated_data['status']
            # if OrderStatus.objects.filter(order=order, status=status).exists():
            #     return Response(
            #         {'error': 'Status already exists for this order'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ShippingAddress model.
    """
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().select_related('user')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # if serializer.validated_data.get('is_default'):
            #     ShippingAddress.objects.filter(user=serializer.validated_data['user']).update(is_default=False)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
