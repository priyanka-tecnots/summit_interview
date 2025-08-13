from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderStatusViewSet, ShippingAddressViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'order-status', OrderStatusViewSet)
router.register(r'shipping-addresses', ShippingAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
