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
    productDate = models.DateTimeField(null=False, auto_now_add=True)
    expiryDate = models.DateField()
    image = models.ImageField(null=True, blank=True, upload_to='produits/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    reserved_quantity = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-productDate']
        verbose_name_plural = 'Products'

    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def stock_status(self):
        available = self.available_quantity()
        if available == 0:
            return 'red'
        elif available <= 5:
            return 'orange'
        else:
            return 'green'
        
    def reserve_stock(self, quantity):
        if quantity > self.available_quantity():
            raise ValueError('insufficient stock available')
        self.reserved_quantity += quantity
        self.save()

    def release_stock(self, quantity):
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.save()

    def consume_stock(self, quantity):
        if quantity > self.reserved_quantity:
            raise ValueError('insufficient stock reserved')
        self.reserved_quantity -= quantity
        self.quantity -= quantity
        self.save()

    def get_snapshot_data(self):
        return {
            'name': self.name,
            'price': float(self.price),
            'batch_number': self.batch_number,
            'expiryDate': self.expiryDate.isoformat(),
        }
    def __str__(self):
        return self.name
