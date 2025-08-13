from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with extended fields.
    """
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    is_customer = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_active_customer(self):
        return self.is_active and self.is_customer
