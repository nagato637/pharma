from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cart, CartStatus
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Cart)
def release_abandoned_cart_stock(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_cart = Cart.objects.get(pk=instance.pk)
            if old_cart.status != instance.status and instance.status == CartStatus.ABANDONED:
                for item in instance.items.all():
                    item.product.release_stock(item.quantity)
        except Cart.DoesNotExist:
            pass