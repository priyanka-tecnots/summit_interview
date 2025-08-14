from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    """
    Product category model.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    """
    Product model.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    image = models.ImageField(upload_to='products/', blank=True)
    
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def get_vendor_name(self):
        return self.vendor.get_full_name()
    
    def get_price_display(self):
        if self.price:
            return f"${self.price}"
        return "Price not available"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{self.id or 'NEW'}-{self.name[:5].upper()}"
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    """
    Product review model.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



class ProductImage(models.Model):
    """
    Product image model for multiple images.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

