from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = ( ('CUSTOMER', 'customer'), ('PHARMACIST', 'pharmacist'), ('MANAGER', 'manager') )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'), related_name='customuser_set', related_query_name='customuser')
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='customuser' )

    class Meta:
        permissions = [('can_view_dashboard', 'can view dashboard') ]

    def __str__(self):
        return self.get_full_name() or self.username

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Customers'
    
    def full_name(self):
        return self.user.get_full_name()

    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.full_name or self.user.username
