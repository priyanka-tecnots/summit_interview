# Summit Market - Intentional Bugs and Issues Documentation

This document catalogs all intentional bugs, security vulnerabilities, and dependency issues added to the Summit Market Django application for testing purposes.

## 🚨 Critical Security Issues

### 1. Hardcoded Secret Key
**File:** `ecommerce/settings.py`
**Issue:** Django secret key is hardcoded in production settings
```python
SECRET_KEY = 'django-insecure-hardcoded-secret-key-for-production-12345'
```
**Impact:** Complete compromise of Django security features including session management, CSRF protection, and password hashing.

### 2. Debug Mode Enabled in Production
**File:** `ecommerce/settings.py`
**Issue:** Debug mode is hardcoded to True
```python
DEBUG = True
```
**Impact:** Exposes sensitive information, error details, and internal system information to users.

### 3. Overly Permissive CORS Configuration
**File:** `ecommerce/settings.py`
**Issue:** CORS allows all origins, methods, and headers
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_METHODS = True
CORS_ALLOW_ALL_HEADERS = True
```
**Impact:** Enables cross-site request forgery attacks and data theft.

### 4. Insecure ALLOWED_HOSTS
**File:** `ecommerce/settings.py`
**Issue:** Wildcard allowed hosts configuration
```python
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '0.0.0.0', 'summit-market.com', '*.summit-market.com']
```
**Impact:** Allows any host to serve the application, enabling host header attacks.

## 🔧 Dependency Issues

### 5. Version Conflicts in requirements.txt
**File:** `requirements.txt`
**Issues:**
- Duplicate packages with conflicting versions:
  - `django-filter==23.5` (appears twice)
  - `django-cors-headers==3.13.0` (appears twice)
  - `django-debug-toolbar==4.2.0` (appears twice)
  - `django-extensions==3.2.3` (appears twice)
  - `python-decouple==3.8` (appears twice)
  - `Pillow==11.3.0` (appears twice)
- Missing critical dependencies for GraphQL and gRPC functionality
- Outdated packages with known security vulnerabilities

### 6. Missing GraphQL Dependencies
**File:** `graphql_schema.py`
**Issue:** GraphQL schema file exists but required dependencies are not in requirements.txt
- Missing: `graphene-django`, `graphene`
**Impact:** GraphQL functionality will fail to import and run.

### 7. Missing gRPC Dependencies
**File:** `grpc_service.py`
**Issue:** gRPC service file exists but required dependencies are not in requirements.txt
- Missing: `grpcio`, `grpcio-tools`, `protobuf`
**Impact:** gRPC functionality will fail to import and run.

## 🐛 Model-Level Bugs

### 8. Phone Number Validation Bug
**File:** `apps/users/models.py`
**Issue:** Phone number regex changed to require exactly 10 digits, breaking international support
```python
phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)
phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
```
**Impact:** Users with international phone numbers cannot register or update their profiles.

### 9. Product Price Nullable Bug
**File:** `apps/products/models.py`
**Issue:** Product price field made nullable, allowing products without prices
```python
price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
```
**Impact:** Products can be created without prices, causing calculation errors in orders.

### 10. SKU Generation Bug
**File:** `apps/products/models.py`
**Issue:** SKU generation in save method references self.id before it exists
```python
def save(self, *args, **kwargs):
    if not self.sku:
        self.sku = f"SKU-{self.id or 'NEW'}-{self.name[:5].upper()}"
    super().save(*args, **kwargs)
```
**Impact:** SKU generation will fail for new products, and 'NEW' will be used instead of actual ID.

### 11. Username Auto-Assignment Bug
**File:** `apps/users/models.py`
**Issue:** Username automatically set to email if not provided
```python
def save(self, *args, **kwargs):
    if not self.username:
        self.username = self.email
    super().save(*args, **kwargs)
```
**Impact:** Creates duplicate usernames if multiple users have the same email, causing database constraint violations.

## 🔄 View-Level Bugs

### 12. Inefficient User Stats Query
**File:** `apps/users/views.py`
**Issue:** User statistics endpoint performs inefficient queries
```python
@action(detail=False, methods=['get'])
def user_stats(self, request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    customers = User.objects.filter(is_customer=True).count()
    vendors = User.objects.filter(is_vendor=True).count()
```
**Impact:** Multiple database queries instead of single aggregated query, poor performance.

### 13. Inefficient Order Stats Query
**File:** `apps/orders/views.py`
**Issue:** Order statistics endpoint performs inefficient calculation
```python
@action(detail=False, methods=['get'])
def order_stats(self, request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    return Response({
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'average_order_value': total_revenue / total_orders if total_orders > 0 else 0
    })
```
**Impact:** Division by zero potential and inefficient query structure.

### 14. Category Slug Generation Bug
**File:** `apps/products/views.py`
**Issue:** Category slug generation without uniqueness check
```python
def create(self, request, *args, **kwargs):
    data = request.data.copy()
    data['slug'] = data.get('name', '').lower().replace(' ', '-')
    request.data = data
    return super().create(request, *args, **kwargs)
```
**Impact:** Creates duplicate slugs, violating unique constraint and causing database errors.

## 🚀 GraphQL Security Issues

### 15. Unrestricted GraphQL Schema
**File:** `graphql_schema.py`
**Issues:**
- All fields exposed without authentication
- No permission checks on mutations
- Direct database access without validation
- Password stored in plain text in mutations
```python
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'  # Exposes all fields including sensitive data
```
**Impact:** Complete data exposure, unauthorized access, and security breaches.

### 16. GraphQL Mutation Security
**File:** `graphql_schema.py`
**Issue:** User creation mutation accepts plain text passwords
```python
def mutate(self, info, username, email, password, first_name=None, last_name=None):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,  # Plain text password
        first_name=first_name or '',
        last_name=last_name or ''
    )
```
**Impact:** Passwords stored in plain text, complete security compromise.

## 🔌 gRPC Security Issues

### 17. Insecure gRPC Server
**File:** `grpc_service.py`
**Issue:** gRPC server runs on insecure port without authentication
```python
server.add_insecure_port('[::]:50051')
```
**Impact:** Unencrypted communication, man-in-the-middle attacks, data interception.

### 18. gRPC Error Information Disclosure
**File:** `grpc_service.py`
**Issue:** Detailed error messages exposed to clients
```python
except Exception as e:
    context.abort(grpc.StatusCode.INTERNAL, str(e))
```
**Impact:** Internal system information leaked to potential attackers.

## ⚡ Celery Task Issues

### 19. Inefficient Database Queries in Tasks
**File:** `celery_tasks.py`
**Issue:** Tasks perform inefficient database operations
```python
total_revenue = sum(order.total_amount for order in Order.objects.filter(status='delivered'))
```
**Impact:** Memory-intensive operations, poor performance, potential timeouts.

### 20. External API Security
**File:** `celery_tasks.py`
**Issue:** External API calls without proper error handling or authentication
```python
response = requests.get(f'https://api.external-inventory.com/product/{product.sku}')
```
**Impact:** Potential data leaks, unauthenticated API access, security vulnerabilities.

### 21. File System Security
**File:** `celery_tasks.py`
**Issue:** File operations without proper path validation
```python
with open(f'daily_report_{yesterday}.json', 'w') as f:
    json.dump(report_data, f)
```
**Impact:** Path traversal attacks, unauthorized file access.

## 🐳 Docker Security Issues

### 22. Insecure Docker Configuration
**File:** `Dockerfile`
**Issue:** Running as root user, no security hardening
```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
**Impact:** Container runs with root privileges, security vulnerabilities.

### 23. Hardcoded Credentials in Docker Compose
**File:** `docker-compose.yml`
**Issue:** Database credentials hardcoded in configuration
```yaml
environment:
  - POSTGRES_PASSWORD=password
  - SECRET_KEY=django-insecure-hardcoded-secret-key-for-production-12345
```
**Impact:** Credentials exposed in version control, security compromise.

### 24. Exposed Database Ports
**File:** `docker-compose.yml`
**Issue:** Database and Redis ports exposed to host
```yaml
ports:
  - "5432:5432"
  - "6379:6379"
```
**Impact:** Direct database access from host, security vulnerability.

## 🔍 Performance Issues

### 25. N+1 Query Problems
**File:** Multiple view files
**Issue:** Related objects not properly prefetched
**Impact:** Poor performance, database overload.

### 26. Synchronous Operations in Async Context
**File:** `celery_tasks.py`
**Issue:** Blocking operations in task processing
```python
time.sleep(1)  # Blocking operation
```
**Impact:** Poor task performance, resource waste.

## 🛡️ Missing Security Features

### 27. No Rate Limiting
**Issue:** No rate limiting on API endpoints
**Impact:** API abuse, DoS attacks.

### 28. No Input Validation
**Issue:** Insufficient input validation in multiple endpoints
**Impact:** Injection attacks, data corruption.

### 29. No Audit Logging
**Issue:** No comprehensive audit logging
**Impact:** No security trail, compliance issues.

### 30. No Data Encryption
**Issue:** Sensitive data not encrypted at rest
**Impact:** Data breaches, compliance violations.

## 📊 Summary

This codebase contains **30+ intentional bugs and security issues** covering:

- **Critical Security Vulnerabilities:** 8 issues
- **Dependency Problems:** 3 issues  
- **Model-Level Bugs:** 4 issues
- **View-Level Issues:** 3 issues
- **GraphQL Security:** 2 issues
- **gRPC Security:** 2 issues
- **Celery Task Issues:** 3 issues
- **Docker Security:** 3 issues
- **Performance Issues:** 2 issues
- **Missing Security Features:** 4 issues

These issues test the candidate's ability to identify and fix:
- Security vulnerabilities
- Performance problems
- Dependency conflicts
- Code quality issues
- Infrastructure security
- API security
- Database optimization
- Error handling
- Input validation
- Authentication and authorization

The candidate should demonstrate expertise in enterprise-grade backend development, security-first design, and modern Python/Django best practices to resolve these issues.
