from django.db import models

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('paid', 'PAID'),
        ('shipped', 'SHIPPED'),
        ('cancelled', 'CANCELLED'), )
    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey()  # Assuming you have a Customer model
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # Assuming you have a Status model

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.order_number} by {self.customer} on {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
