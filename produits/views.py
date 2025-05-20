from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
import os, re
from django.conf import settings
from django.http import JsonResponse


class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()

class AddProduct(CreateView):
    model = Product
    template_name = 'adding.html'
    form_class = AddProductForm
    success_url = reverse_lazy('index')

# fonction pour modifier un produit
# def update(request, id):
#     product = get_object_or_404(Product, id=id)
#     categories = Category.objects.all()
#     errors = {}

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         idcategory = request.POST.get('category')
#         price = request.POST.get('price')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         expiryDate = request.POST.get('expiryDate')
#         image = request.FILES.get('image')

#         if not name:
#             errors['name'] = 'Le nom du produit est requis.'
        
#         if not idcategory:
#             errors['category'] = 'La catégorie du produit est requise.'

#         if not price:
#             errors['price'] = 'Le prix du produit est requis.'

#         if not quantity:
#             errors['quantity'] = 'La quantité du produit est requise.'

#         if not description:
#             errors['description'] = 'la description du produit est requise.'

#         if expiryDate:
#             try:
#                 expiryDate = datetime.strptime(expiryDate, '%Y-%m-%d').date()
#             except ValueError:
#                 errors['expiryDate'] = 'format de date invalide. Utilisez YYYY-MM-DD.'

#         if not errors:
#             category = get_object_or_404(Category, id=idcategory)
            
#             product.name = name
#             product.category = category
#             product.price = price
#             product.quantity = quantity
#             product.description = description
#             product.expiryDate = expiryDate
            
#             if image:
#                 # Spécifier le dossier de destination conformément au paramètre upload_to du modèle
#                 destination = os.path.join(settings.MEDIA_ROOT, 'produits/products/')
#                 fs = FileSystemStorage(location=destination)
#                 # Générer un nom de fichier sécurisé basé sur le nom du produit
#                 save_product_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
#                 extention = os.path.splitext(image.name)[1]
#                 new_filename = f"{save_product_name}{extention}"
#                 # Sauvegarder le fichier et récupérer le nom attribué
#                 filename = fs.save(new_filename, image)
#                 # Enregistrer le chemin relatif dans le modèle (ici, 'produits/products/filename' correspond à la valeur à enregistrer)
#                 product.image.name = os.path.join('produits/products/', filename)
            
#         product.save()
#         messages.success(request, "produit mis à jour avec succès.")
#         return redirect('index')
    
#     else:
#         for error in errors.items():
#             messages.error(request, error)

#     return render(request, 'updating.html', { 'product': product, 'categories': categories, 'errors': errors })

# classe pour modifier un produit
class UpdateProduct(UpdateView):
    model = Product
    template_name = 'update.html'
    form_class = AddProductForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# fonction pour suppression de produit
def delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        product.delete()
        return JsonResponse({ 'success': True, 'message': 'Produit supprimé avec succès.' })
    return JsonResponse({ 'success': False, 'message': 'Erreur lors de la suppression du produit.' })

# fonction pour afficher le produit
# def show(request, id):
#     product = get_object_or_404(Product, id=id)

#     return render(request, 'show.html', { 'product': product })

# class pour afficher le produit
class ShowProduct(DetailView):
    model = Product
    template_name = 'show.html'