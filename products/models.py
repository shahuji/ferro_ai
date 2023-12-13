from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Confirmed', 'Confirmed'),
        ('In Transit', 'In Transit'),
        ('Reached Nearest Hub', 'Reached Nearest Hub'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
        ('Delivery Attempted', 'Delivery Attempted(Failed Delivery)'),
        ('Cancelled', 'Cancelled'),
    ]

    ATTEMPT_CHOICES = [
        (1, 'First Attempt'),
        (2, 'Second Attempt'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, through='Cart')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    attempts = models.PositiveIntegerField(choices=ATTEMPT_CHOICES, default=1)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
