from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from produits.models import Product
from .models import Sale, Customer
from .forms import SaleForm

@transaction.atomic
def add_sell_view(request, id):
    product = get_object_or_404(Product, id=id)
    message = None

    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            customer_name = form.cleaned_data['customer_name']

            if quantity > product.quantity:
                message = f'La quantité ({quantity}) est supérieure au stock disponible ({product.quantity}).'
                form = SaleForm(request.POST)  # Reinitialize form with POST data

            else:
                # récupération ou création du client
                customer, created = Customer.objects.get_or_create(fullname=customer_name)
                total = product.price * quantity

                # création de la vente
                sale = Sale(product=product, quantity=quantity, total=total, customer=customer)
                sale.save()

                # mise à jour du stock du produit
                product.quantity -= quantity
                product.save()

                message = f'Vente de {quantity} {product.name} à {customer.fullname} enregistrée avec succès.'

                return redirect('ventes:invoice', sale_id=sale.id)  # Redirection vers la liste des ventes
    
    else:
        form = SaleForm()

        if product.quantity <= 5:
            message = f'Attention, le stock de ({product.name}-{product.quantity}) est bas !'

    context = { 'product': product, 'form': form, 'message': message }
    
    return render(request, 'addsale.html', context)

def sales(request):
    sales = Sale.objects.all().order_by('-sale_date')  # Récupération des ventes, triées par date décroissante
    context = {'sales': sales }
    return render(request, 'sales.html', context)

def invoice_view(request, id):
    sale = get_object_or_404(Sale, id=id)

    context = {'sale': sale}
    return render(request, 'invoice.html', context)
