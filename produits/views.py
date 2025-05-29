from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()

class AddProduct(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'adding.html'
    form_class = AddProductForm
    success_url = reverse_lazy('produits:index')
    login_url = 'utilisateurs:login'

# classe pour modifier un produit
class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'update.html'
    form_class = AddProductForm
    success_url = reverse_lazy('produits:index')
    login_url = 'utilisateurs:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# class pour suppression de produit
class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('produits:index')
    template_name = 'confirm-delete.html'
    login_url = 'utilisateurs:login'

# class pour afficher le produit
class ShowProduct(DetailView):
    model = Product
    template_name = 'show.html'

# fonction pour rechercher un produit
def search(request):

    queryset = request.GET.get('product', '').strip()
    products = Product.objects.filter(name__icontains=queryset) if queryset else Product.objects.none()
    context = { 'products': products }

    return render(request, 'search.html', context)
