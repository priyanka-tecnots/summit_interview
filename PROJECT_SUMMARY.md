# Django E-commerce Project Summary

## Project Overview

This is a Django REST API project built with clean architecture principles, specifically designed for a **5+ year experience machine test**. The project includes **intentional bugs** that a senior developer should be able to identify and fix.

## Clean Architecture Implementation

### 1. Project Structure
```
ecommerce/
├── apps/                    # Application layer
│   ├── users/              # User management
│   ├── products/           # Product management  
│   └── orders/             # Order management
├── ecommerce/              # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── requirements.txt        # Dependencies
├── manage.py              # Django management
├── README.md              # Project documentation
├── BUGS.md                # List of intentional bugs
└── .gitignore             # Git ignore rules
```

### 2. Clean Architecture Layers

#### Domain Layer (Models)
- **User Model**: Custom user with customer/vendor roles
- **Product Model**: Products with categories, reviews, images
- **Order Model**: Complete order lifecycle with status tracking
- **Supporting Models**: Category, ProductReview, ProductImage, OrderItem, OrderStatus, ShippingAddress

#### Application Layer (Serializers)
- **User Serializers**: UserSerializer, UserListSerializer, UserCreateSerializer
- **Product Serializers**: ProductSerializer, ProductListSerializer, ProductCreateSerializer, CategorySerializer, ProductReviewSerializer
- **Order Serializers**: OrderSerializer, OrderListSerializer, OrderCreateSerializer, OrderItemSerializer, OrderStatusSerializer

#### Interface Layer (Views)
- **User Views**: UserViewSet with custom actions
- **Product Views**: ProductViewSet, CategoryViewSet, ProductReviewViewSet
- **Order Views**: OrderViewSet, OrderItemViewSet, OrderStatusViewSet, ShippingAddressViewSet

#### Infrastructure Layer (Admin, URLs)
- **Admin Interface**: Custom admin configurations for all models
- **URL Routing**: RESTful API endpoints with proper versioning

## Core Features

### 1. User Management
- Custom User model extending AbstractUser
- Customer and vendor role management
- Extended profile fields (phone, address, date of birth)
- User authentication and authorization

### 2. Product Management
- Product catalog with categories
- Product reviews and ratings system
- Multiple product images support
- Stock management
- Vendor-specific products

### 3. Order Management
- Complete order lifecycle (pending → confirmed → processing → shipped → delivered)
- Order items with quantities and pricing
- Order status history tracking
- Shipping address management
- Order cancellation support

### 4. API Features
- RESTful API design
- Comprehensive filtering and search
- Pagination support
- Custom actions for business logic
- Proper HTTP status codes

## Intentional Bugs for Testing

The project contains **50+ intentional bugs** across multiple categories:

### Security Issues (8 bugs)
- Overly permissive CORS settings
- Weak password validation
- Missing permission checks
- Insecure configuration

### Performance Issues (15 bugs)
- Missing database optimizations (select_related, prefetch_related)
- Inefficient queries and N+1 problems
- Missing aggregate functions
- Poor queryset optimization

### Validation Issues (12 bugs)
- Missing model validation methods
- Incomplete serializer validation
- Missing business logic validation
- Missing field-level validation

### Code Quality Issues (10 bugs)
- Missing __str__ methods
- Incomplete admin configurations
- Missing property decorators
- Poor error handling

### Database Issues (5 bugs)
- Missing indexes
- Missing unique constraints
- Inefficient query patterns

### Business Logic Issues (6 bugs)
- Missing stock validation
- Incomplete order status transitions
- Missing vendor permission checks

## API Endpoints

### Users
- `GET/POST /api/v1/users/`
- `GET/PUT/DELETE /api/v1/users/{id}/`
- `GET /api/v1/users/active_users/`
- `POST /api/v1/users/{id}/toggle_status/`

### Products
- `GET/POST /api/v1/products/`
- `GET/PUT/DELETE /api/v1/products/{id}/`
- `GET /api/v1/products/in_stock/`
- `POST /api/v1/products/{id}/add_review/`
- `GET /api/v1/products/top_rated/`

### Categories
- `GET/POST /api/v1/categories/`
- `GET/PUT/DELETE /api/v1/categories/{id}/`
- `GET /api/v1/categories/active/`

### Orders
- `GET/POST /api/v1/orders/`
- `GET/PUT/DELETE /api/v1/orders/{id}/`
- `POST /api/v1/orders/{id}/update_status/`
- `POST /api/v1/orders/{id}/cancel_order/`
- `GET /api/v1/orders/pending_orders/`
- `GET /api/v1/orders/completed_orders/`

## Testing Strategy

### What to Test
1. **Bug Identification**: Find and document all intentional bugs
2. **Bug Fixing**: Implement proper solutions for identified issues
3. **Code Review**: Demonstrate understanding of Django best practices
4. **Performance Optimization**: Improve database queries and API performance
5. **Security Hardening**: Fix security vulnerabilities
6. **Code Quality**: Improve overall code structure and documentation

### Expected Deliverables
1. **Bug Report**: Comprehensive list of identified issues
2. **Fixed Code**: Corrected implementation with proper solutions
3. **Documentation**: Updated documentation reflecting changes
4. **Testing**: Unit tests for critical functionality
5. **Performance Analysis**: Before/after performance metrics

## Evaluation Criteria

A senior developer should demonstrate:

1. **Django Expertise**: Deep understanding of Django ORM, views, serializers
2. **Security Awareness**: Knowledge of common security vulnerabilities
3. **Performance Optimization**: Database query optimization skills
4. **Code Quality**: Clean code principles and best practices
5. **Problem Solving**: Systematic approach to bug identification and fixing
6. **Documentation**: Clear communication of changes and rationale

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start server: `python manage.py runserver`
5. Access admin: `http://localhost:8000/admin/`
6. Explore API: `http://localhost:8000/api/v1/`

## Conclusion

This project provides a comprehensive test of Django development skills, covering security, performance, validation, and code quality. The intentional bugs are designed to test a developer's ability to identify and fix real-world issues that commonly occur in production Django applications.

A successful candidate will demonstrate not only technical proficiency but also attention to detail, understanding of best practices, and ability to write maintainable, secure, and performant code.
