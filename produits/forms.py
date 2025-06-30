# from django.forms import ModelForm
# from .models import Product
# from django import forms

# class AddProductForm(ModelForm):
#     class Meta:
#         model = Product

#         fields = ['name', 'description', 'price', 'quantity', 'expiryDate', 'image', 'category']

#         widgets = {
#             'name': forms.TextInput(attrs = { 'class': 'form-control', 'placeholder': 'nom du produit' }),
#             'description': forms.Textarea(attrs = { 'class': 'form-control', 'placeholder': 'description du produit' }),
#             'price': forms.NumberInput(attrs = { 'class': 'form-control', 'placeholder': 'prix du produit', 'step': 'any' }),
#             'quantity': forms.NumberInput(attrs = { 'class': 'form-control', 'placeholder': 'quantité du produit' }),
#             'expiryDate': forms.DateInput(attrs = { 'class': 'form-control', 'placeholder': 'date d\'expiration du produit', 'type': 'date' }),
#             'image': forms.FileInput(attrs = { 'class': 'form-control-file' }),
#             'category': forms.Select(attrs = { 'class': 'form-control' }),
#         }
