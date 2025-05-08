from django.forms import ModelForm
from .models import Product
from django import forms

class AddProductForm(ModelForm):
    class Meta:
        model = Product

        fields = ['name', 'description', 'price', 'quantity', 'expiryDate', 'image', 'category']

        widgets = {
            'name': forms.TextInput(attrs = { 'class': 'form-control', 'placeholder': 'nom du produit' }),
            'description': forms.Textarea(attrs = { 'class': 'form-control', 'placeholder': 'description du produit' }),
            'price': forms.NumberInput(attrs = { 'class': 'form-control', 'placeholder': 'prix du produit' }),
            'quantity': forms.NumberInput(attrs = { 'class': 'form-control', 'placeholder': 'quantité du produit' }),
            'expiryDate': forms.DateInput(attrs = { 'class': 'form-control', 'placeholder': 'date d\'expiration du produit', 'type': 'date' }),
            'image': forms.FileInput(attrs = { 'class': 'form-control-file' }),
            'category': forms.Select(attrs = { 'class': 'form-control' }),
        }

        def __init__(self, *args, **kwargs):
            super(AddProductForm, self).__init__(*args, **kwargs)
            self.fields['name'].error_message = { 'required': 'le nom est obligatoire', 'invalid': 'ajoutez le nom du produit' }
            self.fields['description'].error_message = { 'required': 'la description est obligatoire', 'invalid': 'ajoutez la description du produit' }
            self.fields['price'].error_message = { 'required': 'le prix est obligatoire', 'invalid': 'ajoutez le prix du produit' }
            self.fields['quantity'].error_message = { 'required': 'la quantité est obligatoire', 'invalid': 'ajoutez la quantité du produit' }
            self.fields['expiryDate'].error_message = { 'required': 'la date d\'expiration est obligatoire', 'invalid': 'ajoutez la date d\'expiration du produit' }
            self.fields['image'].error_message = { 'required': 'l\'image est obligatoire', 'invalid': 'ajoutez l\'image du produit' }
            self.fields['category'].error_message = { 'required': 'la catégorie est obligatoire', 'invalid': 'ajoutez la catégorie du produit' }
