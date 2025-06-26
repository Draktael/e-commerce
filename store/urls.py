from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView,CartCreateAPIView,AddToCartAPIView,UpdateCartItemAPIView,RemoveFromCartAPIView,CartRetrieveDeleteAPIView, OrderListAPIView,OrderDetailAPIView,CreateCheckoutSessionAPIView

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
]   
