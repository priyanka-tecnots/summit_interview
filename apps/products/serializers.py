from rest_framework import serializers
from .models import Category, Product, ProductReview, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    



class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductReview model.
    """
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    



class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'vendor', 'vendor_name', 'image', 'stock_quantity', 'sku',
            'is_active', 'created_at', 'updated_at', 'images', 'reviews', 'average_rating'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'average_rating']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 2)
    



class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product listing.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category_name', 'vendor_name',
            'stock_quantity', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for product creation.
    """
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category', 'vendor',
            'image', 'stock_quantity', 'sku', 'is_active'
        ]
    

