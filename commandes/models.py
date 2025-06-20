import uuid
from django.db import models
from utilisateurs.models import Customer
from produits.models import Product
from django.utils import timezone

class CartStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'active'
    ABANDONED = 'ABANDONED', 'abandoned'
    CANCELLED = 'CANCELLED', 'cancelled'

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'pending'
    PAID = 'PAID', 'paid'
    SHIPPED = 'SHIPPED', 'shipped'
    CANCELLED = 'CANCELLED', 'cancelled'

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CartStatus.choices, default=CartStatus.ACTIVE)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f'Cart {self.id} for {self.customer.full_name}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['cart', 'product']]
        verbose_name_plural = 'Cart Items'

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart {self.cart.id}'

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True ,related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_snapshot = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Orders'

    @property
    def total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart_snapshot['items'])

    def __str__(self):
        return f'Order : ORDER-{self.id.hex[:6].upper()} for {self.customer.full_name if self.customer else 'unknown customer'}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Order Items'

    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.product_name} in order : ORDER-{self.order.id.hex[:6].upper()}'
