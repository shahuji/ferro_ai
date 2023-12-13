from django.urls import path
from .views import ProductList, ProductDetail, UserRegistration, UserLogin, CartView, CartCreate, CartUpdate, CartClear, \
    OrderCreateView, OrderDetailView, OrderUpdateView, CartList, OrderList

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('products/list/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('cart/list/', CartList.as_view(), name='cart-list'),
    path('cart/add/', CartCreate.as_view(), name='cart-add'),
    path('cart/update/<int:pk>/', CartUpdate.as_view(), name='cart-update'),
    path('cart/view/', CartView.as_view(), name='cart-view'),
    path('cart/clear/', CartClear.as_view(), name='cart-clear'),
    path('order/list/', OrderList.as_view(), name='order-list'),
    path('order/add/', OrderCreateView.as_view(), name='create_order'),
    path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
]
