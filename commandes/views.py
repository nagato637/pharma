from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from produits.models import *
from commandes.models import *

from django.db import transaction

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id) 
    customer = request.user.customer
    
    cart, created = Cart.objects.get_or_create(customer=customer, status=CartStatus.ACTIVE)

    # check if product stock is sufficient
    if product.available_quantity() < 1:
        messages.error(request, f'insufficient stock of {product.name}')
        return redirect('produits:detail', product_id=product_id)
    
    try:
        with transaction.atomic():
            locked_product = Product.objects.select_for_update().get(pk=product_id)
            locked_product.reserve_stock(1)
            locked_product.save()
    except Exception as e:
        messages.error(request, f'erreur de reservation de stock: {str(e)}')
        return redirect('produits:details', product_id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, 'produit ajouté au panier')
    return redirect('commandes:cart_detail')

def get_active_cart(user):
    return Cart.objects.get(customer=user.customer, status=CartStatus.ACTIVE)
    
def checkout(request):
    try:
        cart = get_active_cart(request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'aucun panier actif')
        return redirect('produits:index')

    # validation du stock
    for item in cart.items.all(): # type: ignore
        if item.quantity > item.product.available_quantity():
            messages.error(request, f'stock insuffisant pour {item.product.name} - disponible : {item.product.available_quantity()}')
            return redirect('commandes:cart_detail')
    
    # création de la commande
    try:
        with transaction.atomic():
            order = Order.objects.create(customer=request.user.customer)

            # création des articles commandés
            for cart_item in cart.items.all(): # type: ignore
                product = cart_item.product
                OrderItem.objects.create(order=order, product_name=product.name, unit_price=product.price, quantity=cart_item.quantity, batch_number=product.batch_number, expiry_date=product.expiryDate)

                # consummer le stock
                product.consume_stock(cart_item.quantity)
            
            cart.status = CartStatus.CONVERTED
            cart.save()

    except Exception as e:
        messages.error(request, f'erreur lors de la commande: {str(e)}')
        return redirect('commandes:cart_detail')

    return redirect('commandes:order_detail', order_id=order.id)
