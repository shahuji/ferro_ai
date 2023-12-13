from django.urls import path
from .views import ProductList, ProductDetail, UserRegistration, UserLogin, CartView, CartCreate, CartUpdate, CartClear

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('cart/add/', CartCreate.as_view(), name='cart-add'),
    path('cart/update/<int:pk>/', CartUpdate.as_view(), name='cart-update'),
    path('cart/view/', CartView.as_view(), name='cart-view'),
    path('cart/clear/', CartClear.as_view(), name='cart-clear'),
]
