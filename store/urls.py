from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductListAPIView, ProductDetailAPIView,CartCreateAPIView,AddToCartAPIView,UpdateCartItemAPIView,RemoveFromCartAPIView,CartRetrieveDeleteAPIView, OrderListAPIView,OrderDetailAPIView,CreateCheckoutSessionAPIView,RegisterUserAPIView, UserMeView, HistoryOrdersAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/',ProductDetailAPIView.as_view(), name='product-detail'),
    path('cart/create/', CartCreateAPIView.as_view(), name='cart-create'),
    path('cart/<int:pk>/',CartRetrieveDeleteAPIView.as_view(), name='cart-retrieve-delete'),
    path('cart/<int:cart_id>/add/', AddToCartAPIView.as_view(), name='cart-add'),
    path('cart/<int:cart_id>/update/',UpdateCartItemAPIView.as_view(), name='cart-update'),
    path('cart/<int:cart_id>/remove/',RemoveFromCartAPIView.as_view(), name='cart-remove'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),            # opcional
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('checkout/<int:cart_id>/', CreateCheckoutSessionAPIView.as_view(), name='checkout-session'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view(), name='register-user'), # Ruta para el registro de usuarios
    path('me/', UserMeView.as_view(), name='user-me'),  # Ruta para obtener información del usuario autenticado
    path('history-orders/', HistoryOrdersAPIView.as_view(), name='history-orders'),  # Ruta para obtener el historial de pedidos del usuario autenticado
]