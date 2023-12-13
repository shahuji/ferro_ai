from rest_framework import serializers

from .models import Product, Cart, Order

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not User.objects.filter(email=email, is_superuser=False).exists():
            raise serializers.ValidationError('Invalid email or password.')
        else:
            email = User.objects.filter(email=email).first().username

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.')

        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
