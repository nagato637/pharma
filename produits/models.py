from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    productDate = models.DateField(auto_now_add=True)
    expiryDate = models.DateField()
    image = models.ImageField(null=True, blank=True, upload_to='produits/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-productDate']

    def quantity_available(self):
        if self.quantity == 0:
            return 'red'
        elif self.quantity <= 5:
            return 'orange'
        else:
            return 'green'

    def __str__(self):
        return self.name

