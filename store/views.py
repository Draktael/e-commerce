import stripe
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Cart, CartItem,Order
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, UserSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartCreateAPIView(APIView):
    def post(slef, request):
        cart = Cart.objects.create()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class CartRetrieveDeleteAPIView(APIView):
    def get(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        return Response(CartSerializer(cart).data)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        cart.delete()
        return Response(status=204)

class AddToCartAPIView(APIView):
    def post(self, request, cart_id):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

       
        cart, created = Cart.objects.get_or_create(pk=cart_id)

        product = get_object_or_404(Product, pk=product_id)

        item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created_item:
            item.quantity += int(quantity)
            item.save()

        return Response(CartSerializer(cart).data, status=200)
    
from rest_framework.exceptions import NotFound

class UpdateCartItemAPIView(APIView):
    def put(self, request, cart_id):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({"detail": "Faltan campos product_id o quantity."}, status=400)

        # Buscar carrito
        cart = get_object_or_404(Cart, pk=cart_id)

        # Intentar encontrar el item del carrito
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            raise NotFound(detail="Este producto no está en el carrito.")

        # Validar cantidad
        if int(quantity) < 1:
            return Response({"detail": "La cantidad debe ser al menos 1."}, status=400)

        # Actualizar cantidad
        item.quantity = int(quantity)
        item.save()

        return Response(CartSerializer(cart).data, status=200)

    
class RemoveFromCartAPIView(APIView):
    def delete(self, request, cart_id):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"detail": "Se requiere product_id."}, status=400)

        cart = get_object_or_404(Cart, pk=cart_id)
        product = get_object_or_404(Product, pk=product_id)
        item = get_object_or_404(CartItem, cart=cart, product=product)
        item.delete()

        return Response(CartSerializer(cart).data, status=200)
    
class CreateCheckoutSessionAPIView(APIView):
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, pk = cart_id)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"detail:" "El carrito esta vacio"}, status=400)
        
        total = sum(item.product.price * item.quantity for item in cart_items)

        order, created = Order.objects.get_or_create(
            cart = cart,
            defaults={'total': total}
        )

        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),  # convertir a centavos
                },
                'quantity': item.quantity,
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items,
                metadata={'order_id': str(order.id)},
                success_url='http://localhost:3000/success/',
                cancel_url='http://localhost:3000/cancel/',
            )
            return Response({'checkout_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class RegisterUserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"detail": "Faltan campos requeridos."}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"detail": "Usuario creado exitosamente."}, status=201)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
