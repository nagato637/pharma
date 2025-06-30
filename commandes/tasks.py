from django.utils import timezone
from .models import Cart, CartStatus
from django_q.tasks import schedule

def cleanup_abandoned_carts():
    expired_date = timezone.now() - timezone.timedelta(days=3)
    abondoned_carts = Cart.objects.filter(status=CartStatus.ABANDONED, update_at__lt=expired_date)

    for cart in abondoned_carts:
        for item in cart.items.all(): # type: ignore
            item.product.released_stock(item.quantity)
        cart.delete()

schedule('commandes.tasks.cleanup_abandoned_carts', schedule_type='D', repeats=-1)
