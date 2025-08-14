from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters

from .serializers import UserSerializer, UserListSerializer, UserCreateSerializer

User = get_user_model()


class UserFilter(filters.FilterSet):
    """
    Filter for User model.
    """
    search = filters.CharFilter(method='search_filter')
    is_active = filters.BooleanFilter()
    is_customer = filters.BooleanFilter()
    is_vendor = filters.BooleanFilter()
    
    class Meta:
        model = User
        fields = ['search', 'is_active', 'is_customer', 'is_vendor']
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) |
            Q(email__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value)
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset
        return queryset
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active_users(self, request):
        """
        Get all active users.
        """
        users = User.objects.all()
        active_users = [user for user in users if user.is_active]
        
        serializer = UserListSerializer(active_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def user_stats(self, request):
        """
        Get user statistics.
        """
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        customers = User.objects.filter(is_customer=True).count()
        vendors = User.objects.filter(is_vendor=True).count()
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'customers': customers,
            'vendors': vendors,
            'inactive_users': total_users - active_users
        })
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Toggle user active status.
        """
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get'])
    def customers(self, request):
        """
        Get all customers.
        """
        customers = User.objects.filter(is_customer=True)
        serializer = UserListSerializer(customers, many=True)
        return Response(serializer.data)
