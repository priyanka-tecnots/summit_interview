# Django E-commerce API

A Django REST API project built with clean architecture principles for managing users, products, and orders.

## Features

- **User Management**: Custom user model with customer/vendor roles
- **Product Management**: Products with categories, reviews, and images
- **Order Management**: Complete order lifecycle with status tracking
- **REST API**: Full CRUD operations with filtering and search
- **Admin Interface**: Django admin with custom configurations
- **Clean Architecture**: Well-organized code structure

## Project Structure

```
ecommerce/
├── apps/
│   ├── users/           # User management app
│   ├── products/        # Product management app
│   └── orders/          # Order management app
├── ecommerce/           # Main project settings
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}/` - Get user details
- `PUT /api/v1/users/{id}/` - Update user
- `DELETE /api/v1/users/{id}/` - Delete user

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{id}/` - Get product details
- `PUT /api/v1/products/{id}/` - Update product
- `DELETE /api/v1/products/{id}/` - Delete product

### Categories
- `GET /api/v1/categories/` - List categories
- `POST /api/v1/categories/` - Create category
- `GET /api/v1/categories/{id}/` - Get category details

### Orders
- `GET /api/v1/orders/` - List orders
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/{id}/` - Get order details
- `PUT /api/v1/orders/{id}/` - Update order
- `POST /api/v1/orders/{id}/update_status/` - Update order status

## Models

### User
- Custom user model extending AbstractUser
- Customer and vendor roles
- Extended profile fields

### Product
- Product information with categories
- Stock management
- Product reviews and ratings
- Multiple product images

### Order
- Complete order lifecycle
- Order items with quantities
- Status tracking
- Shipping address management

## Clean Architecture

The project follows clean architecture principles:

- **Models**: Data layer with Django ORM
- **Serializers**: Data transformation layer
- **Views**: Business logic layer
- **URLs**: Routing layer
- **Admin**: Interface layer

## Testing

Run tests:
```bash
python manage.py test
```

## Known Issues

This project contains intentional bugs for testing purposes:

1. **Security Issues**:
   - Overly permissive CORS settings
   - Weak password validation
   - Missing permission checks

2. **Performance Issues**:
   - Missing database optimizations
   - Inefficient queries
   - Missing select_related/prefetch_related

3. **Validation Issues**:
   - Missing field validations
   - Incomplete error handling
   - Missing business logic validations

4. **Code Quality Issues**:
   - Missing __str__ methods
   - Incomplete admin configurations
   - Missing proper documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
