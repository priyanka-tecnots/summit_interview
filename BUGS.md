# Intentional Bugs for Machine Test

This document lists all the intentional bugs that have been placed in the codebase for testing purposes. A senior developer should be able to identify and fix these issues.

## Security Issues

### 1. Settings Configuration
- **File**: `ecommerce/settings.py`
- **Issue**: Overly permissive CORS settings (`CORS_ALLOW_ALL_ORIGINS = True`)
- **Issue**: Weak password validation (min_length=8)
- **Issue**: Overly permissive ALLOWED_HOSTS (`['*']`)

### 2. User Model
- **File**: `apps/users/models.py`
- **Issue**: Missing `null=True` for optional fields like `profile_picture`
- **Issue**: Missing `__str__` method
- **Issue**: Missing `clean()` method for validation
- **Issue**: Missing `@property` decorator for `is_active_customer` method

### 3. User Serializers
- **File**: `apps/users/serializers.py`
- **Issue**: Commented out password validation in `validate_password`
- **Issue**: Missing email uniqueness validation in `UserCreateSerializer`
- **Issue**: Inefficient `get_full_name` method (should use select_related)

### 4. User Views
- **File**: `apps/users/views.py`
- **Issue**: Missing permission checks for sensitive operations
- **Issue**: Inefficient queryset (missing select_related)
- **Issue**: Inefficient `active_users` action (should use filter instead of list comprehension)
- **Issue**: Missing proper error handling in create method

## Performance Issues

### 1. Product Models
- **File**: `apps/products/models.py`
- **Issue**: Missing `__str__` methods
- **Issue**: Missing `@property` for `is_available`
- **Issue**: Inefficient `get_vendor_name` method
- **Issue**: Missing `clean()` methods for validation

### 2. Product Serializers
- **File**: `apps/products/serializers.py`
- **Issue**: Inefficient `get_average_rating` method (should use aggregate)
- **Issue**: Missing validation methods
- **Issue**: Missing SKU generation in create method

### 3. Product Views
- **File**: `apps/products/views.py`
- **Issue**: Inefficient queryset (missing select_related and prefetch_related)
- **Issue**: Inefficient `in_stock` action (should use filter)
- **Issue**: Inefficient `top_rated` action (should use aggregate)
- **Issue**: Missing validation in `update_stock` action

### 4. Order Models
- **File**: `apps/orders/models.py`
- **Issue**: Missing `__str__` methods
- **Issue**: Missing `@property` for `is_completed`
- **Issue**: Missing `calculate_total` method
- **Issue**: Missing `save()` method for order number generation

### 5. Order Serializers
- **File**: `apps/orders/serializers.py`
- **Issue**: Inefficient `get_items_count` method (should use annotate)
- **Issue**: Missing validation methods
- **Issue**: Missing create method for order and items
- **Issue**: Missing validation for status transitions

### 6. Order Views
- **File**: `apps/orders/views.py`
- **Issue**: Inefficient queryset (missing select_related and prefetch_related)
- **Issue**: Inefficient `pending_orders` action (should use filter)
- **Issue**: Missing status history creation in `update_status`
- **Issue**: Missing validation in `cancel_order`

## Validation Issues

### 1. Model Validation
- **Issue**: Missing `clean()` methods across all models
- **Issue**: Missing field validators (price, quantity, etc.)
- **Issue**: Missing unique constraints (e.g., user-product review combination)

### 2. Serializer Validation
- **Issue**: Missing validation for required fields
- **Issue**: Missing business logic validation
- **Issue**: Missing custom validation methods

### 3. View Validation
- **Issue**: Missing permission checks
- **Issue**: Missing input validation
- **Issue**: Missing business rule validation

## Code Quality Issues

### 1. Admin Configuration
- **File**: `apps/*/admin.py`
- **Issue**: Missing `fieldsets` configuration
- **Issue**: Missing `list_editable` for quick editing
- **Issue**: Missing `prepopulated_fields` for slugs
- **Issue**: Missing custom admin actions
- **Issue**: Missing `readonly_fields`

### 2. Missing Methods
- **Issue**: Missing `__str__` methods in all models
- **Issue**: Missing `save()` methods for auto-generation
- **Issue**: Missing `clean()` methods for validation
- **Issue**: Missing `@property` decorators

### 3. Documentation
- **Issue**: Missing docstrings in some methods
- **Issue**: Missing help_text in model fields
- **Issue**: Missing verbose_name in model Meta classes

## Database Issues

### 1. Missing Indexes
- **Issue**: No database indexes on frequently queried fields
- **Issue**: Missing unique constraints where needed

### 2. Query Optimization
- **Issue**: Missing `select_related` and `prefetch_related`
- **Issue**: N+1 query problems
- **Issue**: Inefficient aggregate queries

## Business Logic Issues

### 1. Order Management
- **Issue**: Missing stock validation when creating orders
- **Issue**: Missing order status transition validation
- **Issue**: Missing total calculation logic

### 2. Product Management
- **Issue**: Missing vendor permission validation
- **Issue**: Missing stock update logic
- **Issue**: Missing price validation

### 3. User Management
- **Issue**: Missing role validation
- **Issue**: Missing customer/vendor permission checks

## Error Handling Issues

### 1. Exception Handling
- **Issue**: Missing proper exception handling in views
- **Issue**: Missing custom exception classes
- **Issue**: Missing proper error responses

### 2. Validation Errors
- **Issue**: Missing custom validation error messages
- **Issue**: Missing field-level error handling

## Testing Issues

### 1. Missing Tests
- **Issue**: No test files included
- **Issue**: Missing unit tests for models
- **Issue**: Missing integration tests for views
- **Issue**: Missing API tests

## Deployment Issues

### 1. Production Settings
- **Issue**: Debug mode enabled in production
- **Issue**: Missing production database configuration
- **Issue**: Missing static file configuration
- **Issue**: Missing media file serving configuration

## Summary

This codebase contains approximately **50+ intentional bugs** across different categories:

- **Security**: 8 bugs
- **Performance**: 15 bugs
- **Validation**: 12 bugs
- **Code Quality**: 10 bugs
- **Database**: 5 bugs
- **Business Logic**: 6 bugs
- **Error Handling**: 4 bugs
- **Testing**: 4 bugs
- **Deployment**: 4 bugs

A senior developer should be able to identify and fix these issues systematically, demonstrating their understanding of Django best practices, security considerations, performance optimization, and clean code principles.
