from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=0)
    productDate = models.DateTimeField(auto_now_add=True)
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

class Order (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name} on {self.orderDate}"
    

class Receipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receiptDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.order.product.name} on {self.receiptDate}"
    
