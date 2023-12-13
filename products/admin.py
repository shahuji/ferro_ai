from django.contrib import admin
from products.models import Product, Order, Cart


# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
