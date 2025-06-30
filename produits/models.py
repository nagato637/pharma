from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Product(models.Model):
    FORME_CHOICES = (
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('LIQUID', 'Liquid'),
        ('CREAM', 'Cream'),
        ('INJECTION', 'injection'),
        ('DROPS', 'Drops'), )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    batch_number = models.CharField(max_length=100)
    reserved_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    requires_prescription = models.BooleanField(default=False)
    dosage = models.CharField(max_length=255, blank=True)
    form = models.CharField(max_length=20, choices=FORME_CHOICES, blank=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'batch_number']),
            models.Index(fields=['expiry_date'])
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_non_negative'),
            models.CheckConstraint(check=models.Q(reserved_quantity__lte=models.F('quantity')), name='reserved_lte_total'),
        ]
        verbose_name_plural = 'Products'

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def expires_soon(self):
        return (self.expiry_date - timezone.now().date()).days <= 30
           
    def reserve_stock(self, quantity):
        if quantity > self.available_quantity:
            raise ValidationError('insufficient stock available')
        self.reserved_quantity += quantity
        self.save()

    def release_stock(self, quantity):
        if quantity > self.reserved_quantity:
            quantity = self.reserved_quantity
        self.reserved_quantity -= quantity
        self.save()

    def consume_stock(self, quantity):
        if quantity > self.reserved_quantity:
            raise ValidationError('insufficient stock reserved')
        self.reserved_quantity -= quantity
        self.quantity -= quantity
        self.save()

    def clean(self):
        if self.expiry_date < timezone.now().date():
            raise ValidationError(_('ce produit est périmé'))
        if self.reserved_quantity > self.quantity:
            raise ValidationError(_('la quantité peut pas dépasser le stock'))

    def __str__(self):
        return f'{self.name} ({self.batch_number})' if self.batch_number else self.name
    