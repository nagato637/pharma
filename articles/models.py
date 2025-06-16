from django.db import models
from produits.models import Product

class Item(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    variant = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
 

class Cart(models.Model):
    items = models.ManyToManyField(Item, blank=True, related_name='carts')

    def __str__(self):
        return f"Cart {self.id} with {self.items.count()} items"
