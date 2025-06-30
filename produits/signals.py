from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product
from django.utils import timezone

@receiver(pre_save, sender=Product)
def check_product_expiry(sender, instance, **kwargs):
    if instance.expiry_date < timezone.now().date():
        instance.is_active = False
