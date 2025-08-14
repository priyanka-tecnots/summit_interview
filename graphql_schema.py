import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from apps.products.models import Product, Category
from apps.orders.models import Order, OrderItem

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = '__all__'


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))
    order_by_id = graphene.Field(OrderType, id=graphene.Int(required=True))
    
    def resolve_all_users(self, info):
        return User.objects.all()
    
    def resolve_all_products(self, info):
        return Product.objects.all()
    
    def resolve_all_orders(self, info):
        return Order.objects.all()
    
    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)
    
    def resolve_product_by_id(self, info, id):
        return Product.objects.get(id=id)
    
    def resolve_order_by_id(self, info, id):
        return Order.objects.get(id=id)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, username, email, password, first_name=None, last_name=None):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name or '',
            last_name=last_name or ''
        )
        return CreateUser(user=user)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        category_id = graphene.Int(required=True)
        vendor_id = graphene.Int(required=True)
        stock_quantity = graphene.Int()
    
    product = graphene.Field(ProductType)
    
    def mutate(self, info, name, description, price, category_id, vendor_id, stock_quantity=0):
        category = Category.objects.get(id=category_id)
        vendor = User.objects.get(id=vendor_id)
        
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            vendor=vendor,
            stock_quantity=stock_quantity
        )
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        shipping_address = graphene.String(required=True)
        billing_address = graphene.String(required=True)
        items = graphene.List(graphene.Int, required=True)
        quantities = graphene.List(graphene.Int, required=True)
    
    order = graphene.Field(OrderType)
    
    def mutate(self, info, customer_id, shipping_address, billing_address, items, quantities):
        customer = User.objects.get(id=customer_id)
        
        order = Order.objects.create(
            customer=customer,
            shipping_address=shipping_address,
            billing_address=billing_address,
            subtotal=0,
            tax_amount=0,
            shipping_cost=0,
            total_amount=0
        )
        
        total = 0
        for i, product_id in enumerate(items):
            product = Product.objects.get(id=product_id)
            quantity = quantities[i] if i < len(quantities) else 1
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price or 0,
                total_price=(product.price or 0) * quantity
            )
            total += (product.price or 0) * quantity
        
        order.subtotal = total
        order.tax_amount = total * 0.1
        order.shipping_cost = 10.0
        order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost
        order.save()
        
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
