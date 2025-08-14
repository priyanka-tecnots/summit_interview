import grpc
from concurrent import futures
import time
import json
import sqlite3
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.orders.models import Order

User = get_user_model()

# Import the generated gRPC code
import summit_market_pb2
import summit_market_pb2_grpc


class SummitMarketService(summit_market_pb2_grpc.SummitMarketServiceServicer):
    
    def GetUser(self, request, context):
        try:
            user = User.objects.get(id=request.user_id)
            return summit_market_pb2.UserResponse(
                user_id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active
            )
        except User.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User not found')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def CreateUser(self, request, context):
        try:
            user = User.objects.create_user(
                username=request.username,
                email=request.email,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name
            )
            return summit_market_pb2.UserResponse(
                user_id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.product_id)
            return summit_market_pb2.ProductResponse(
                product_id=product.id,
                name=product.name,
                description=product.description,
                price=str(product.price or 0),
                stock_quantity=product.stock_quantity,
                vendor_id=product.vendor.id
            )
        except Product.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Product not found')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def CreateProduct(self, request, context):
        try:
            vendor = User.objects.get(id=request.vendor_id)
            product = Product.objects.create(
                name=request.name,
                description=request.description,
                price=request.price,
                vendor=vendor,
                stock_quantity=request.stock_quantity
            )
            return summit_market_pb2.ProductResponse(
                product_id=product.id,
                name=product.name,
                description=product.description,
                price=str(product.price or 0),
                stock_quantity=product.stock_quantity,
                vendor_id=product.vendor.id
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetOrder(self, request, context):
        try:
            order = Order.objects.get(id=request.order_id)
            return summit_market_pb2.OrderResponse(
                order_id=order.id,
                customer_id=order.customer.id,
                status=order.status,
                total_amount=str(order.total_amount),
                created_at=order.created_at.isoformat()
            )
        except Order.DoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Order not found')
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def CreateOrder(self, request, context):
        try:
            customer = User.objects.get(id=request.customer_id)
            
            order = Order.objects.create(
                customer=customer,
                shipping_address=request.shipping_address,
                billing_address=request.billing_address,
                subtotal=0,
                tax_amount=0,
                shipping_cost=0,
                total_amount=0
            )
            
            total = 0
            for item in request.items:
                product = Product.objects.get(id=item.product_id)
                total += (product.price or 0) * item.quantity
            
            order.subtotal = total
            order.tax_amount = total * 0.1
            order.shipping_cost = 10.0
            order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost
            order.save()
            
            return summit_market_pb2.OrderResponse(
                order_id=order.id,
                customer_id=order.customer.id,
                status=order.status,
                total_amount=str(order.total_amount),
                created_at=order.created_at.isoformat()
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetUserStats(self, request, context):
        try:
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            
            return summit_market_pb2.UserStatsResponse(
                total_users=total_users,
                active_users=active_users,
                inactive_users=total_users - active_users
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def GetOrderStats(self, request, context):
        try:
            total_orders = Order.objects.count()
            total_revenue = sum(order.total_amount for order in Order.objects.filter(status='delivered'))
            
            return summit_market_pb2.OrderStatsResponse(
                total_orders=total_orders,
                total_revenue=str(total_revenue),
                average_order_value=str(total_revenue / total_orders if total_orders > 0 else 0)
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    summit_market_pb2_grpc.add_SummitMarketServiceServicer_to_server(
        SummitMarketService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
