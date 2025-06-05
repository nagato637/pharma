from django.db import models
from produits.models import Product

class Customer(models.Model):
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places = 2)

    def __str__(self):
        return f'Vente de {self.quantity} {self.product.name} à {self.customer.fullname} le {self.sale_date.strftime("%Y-%m-%d")}'
