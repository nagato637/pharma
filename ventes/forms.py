from django import forms

class SaleForm(forms.Form):

    quantity = forms.IntegerField(label='quantité', min_value=1, required=True, widget=forms.NumberInput(attrs={ 'placeholder': 'quantité du produit', 'class': 'forms-control' }))
    customer_name = forms.CharField(label='client', max_length=255, required=True, widget=forms.TextInput(attrs={ 'placeholder': 'nom du client', 'class': 'forms-control' }))
