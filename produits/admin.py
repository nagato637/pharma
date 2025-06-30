from django.contrib import admin
from django.utils import timezone
from .models import Product, Category

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'expiry_date', 'available_quantity', 'price', 'is_active')
    list_filter = ('category', 'is_active', 'requires_prescription')
    search_fields = ('name', 'batch_number', 'barcode')
    readonly_fields = ('available_quantity', 'is_expired')
    actions = ['desactivate_products']

    def desactivate_expired(self, request, queryset):
        queryset.filter(expiry_date__lt=timezone.now().date()).update(is_active=False)
    
    desactivate_expired.short_description = 'Desactivate expired products'

admin.site.register(Category)