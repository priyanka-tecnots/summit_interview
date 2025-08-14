from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'date_of_birth', 'profile_picture',
            'is_customer', 'is_vendor', 'is_active', 'created_at', 'updated_at',
            'password', 'password_confirm'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs.get('password') and not attrs.get('password_confirm'):
            raise serializers.ValidationError("Password confirmation is required")
        
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match")
        
        return attrs
    
    def validate_password(self, value):
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user listing.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'is_customer', 'is_vendor', 'is_active']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
