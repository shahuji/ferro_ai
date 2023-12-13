from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order


@receiver(pre_save, sender=Order)
def update_order_status(sender, instance, **kwargs):
    if instance.status == 'Delivery Attempted' and instance.attempts == 1:
        instance.status = 'Reached Nearest Hub'
        instance.attempts = 2
    elif instance.status == 'Delivery Attempted' and instance.attempts == 2:
        instance.status = 'Cancelled'


@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock_quantity -= instance.quantity
        product.save()
