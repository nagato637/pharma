from django.shortcuts import render, get_object_or_404, HttpResponse
from produits.models import *
from commandes.models import *

def add_to_cart(request, product_id):
    product = Product.objects.get_object_or_404(pk=product_id)
    # cart, _ = Cart.objects.get_or_create(customer=request.user.customer, status=CartStatus.ACTIVE)

    # # check if product stock is sufficient
    # if product.available_quantity < 1:
    #     return HttpResponse('Product is out of stock', status=400)
    
    # # reserve the stock
    # product.reserve
    # return render(request, 'add_to_cart.html')