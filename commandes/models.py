import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from utilisateurs.models import Customer
from produits.models import Product

class CartStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'active'
    ABANDONED = 'ABANDONED', 'abandoned'
    CONVERTED = 'CONVERTED', 'converted'

class OrderStatus(models.TextChoices):
    CREATED = 'CREATED', 'created'
    PAID = 'PAID', 'paid'
    SHIPPED = 'SHIPPED', 'shipped'
    CANCELLED = 'CANCELLED', 'cancelled'
    REFUNDED = 'REFUNDED', 'refunded'

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CartStatus.choices, default=CartStatus.ACTIVE)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=3))

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Carts'
        indexes = [models.Index(fields=['status', 'expires_at']), ]

    def __str__(self):
        return f'Cart {self.id.hex[:6]} for {self.customer.full_name}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['cart', 'product']]
        verbose_name_plural = 'Cart Items'

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED, verbose_name='statut')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    prescription_required = models.BooleanField(default=False)
    # cart_snapshot = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Orders'
        permissions = [ ('can_manage_order') ]

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all()) # type: ignore

    def __str__(self):
        return f'Order : ORDER-{self.id.hex[:6].upper()} for {self.customer.full_name if self.customer else 'unknown customer'}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    dosage = models.CharField(max_length=50, blank=True)
    form = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Order Items'

    @property
    def total_price(self):
        if self.unit_price is None:
            return 0
        
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product_name} in order : ORDER-{self.order.id.hex[:6].upper()}'
