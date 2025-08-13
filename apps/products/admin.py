from django.contrib import admin
from .models import Category, Product, ProductReview, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category model.
    """
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin for Product model.
    """
    list_display = ['name', 'category', 'vendor', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'vendor', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'sku']
    ordering = ['-created_at']
    
    def get_vendor_name(self, obj):
        return obj.vendor.get_full_name()
    get_vendor_name.short_description = 'Vendor'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """
    Admin for ProductReview model.
    """
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    ordering = ['-created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'User'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin for ProductImage model.
    """
    list_display = ['product', 'alt_text', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    ordering = ['-created_at']
    

