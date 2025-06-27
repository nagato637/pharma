from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from produits.models import *
from commandes.models import *

from django.db import transaction
from django.db.models import pre_save

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, _ = Cart.objects.get_or_create(customer=request.user.customer, status=CartStatus.ACTIVE)

    # check if product stock is sufficient
    if product.available_quantity() < 1:
        return HttpResponse('Product is out of stock', status=400)
    
    # reserve the stock 
    product.reserve_stock(quantity=1)

    # add to cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
def checkout(request):
    cart = get_active_cart(request.user)

    # validation du stock
    for item in cart.items.all():
        if item.quantity > item.product.available_quantity():
            return render_error(f'insufficient stock of {item.product.name} ... choose another one')
        
    # création de la commande
    order = Order.objects.create(customer=request.user.customer)
    # création des OrderItems avec données figées
    for cart_item in cart.items.all():
        product = cart_item.product
        OrderItem.objects.create(order=order, product_name=product.name, unit_price=product.price, quantity=cart_item.quantity, batch_number=product.batch_number, expiry_date=product.expiryDate)
        product.consume_stock(cart_item.quantity)

    cart.statut = CartStatus.CONVERTED
    cart.save()

    return redirect('payment', order_id=order.id)

# ==================================================

# implémentation du looking transactionel
with transaction.atomic():
    product = Product.objects.select_for_update().get(id=product_id)


# ajouter des signaux pour nettoyer les paniers abandonnés
def release_abandoned_cart_stock(sender, instance, **kwargs):
    if instance.status == CartStatus.ABANDONED:
        for item in instance.items.all():
            item.product.release_stock(item.quantity)

pre_save.connect(release_abandoned_cart_stock, sender=Cart)

def clean(self):
    if self.expiry_date < date.today():
        raise ValidationError(f'{product.name} est périmé et interdit à la vente')