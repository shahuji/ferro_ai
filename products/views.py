from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .permissions import IsStaffUser
from .models import Product, Cart, Order
from products.serializers import ProductSerializer, UserSerializer, UserLoginSerializer, CartSerializer, OrderSerializer

from django.contrib.auth import get_user_model


User = get_user_model()


# Create your views here.

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        Token.objects.create(user=user)


class UserLogin(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if user is not None:
            Token.objects.get_or_create(user=user)
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CartCreate(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class CartUpdate(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]


class CartView(generics.ListAPIView):
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class CartClear(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='Placed')


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return self.queryset.filter(user=user)
        else:
            return self.queryset.filter(status='Reached Nearest Hub')


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]
