from django.shortcuts import render
from django.views.generic import ListView
from .models import *

def index(request):
    products = Product.objects.all()
    context = { 'products': products }

    return render(request, 'index.html', context)

class HomeView(ListView):
    template_name = 'index.html'    # spécifie le template à utiliser
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()

def addProduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # recuperer la clé étrangère de la catégorie
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id) if category_id else None
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        expiryDate = request.POST.get('expiryDate')
        image = request.FILES.get('image')
        # Créer un nouvel objet Product
        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            expiryDate=expiryDate,
            image=image,
            category=category
        )
        # Enregistrer l'objet dans la base de données
        product.save()
        # Rediriger vers la page d'accueil ou afficher un message de succès
        return render(request, 'index.html', {'success': True})
    else:
        categories = Category.objects.all()
        return render(request, 'addproduct.html', {'categories': categories})
    