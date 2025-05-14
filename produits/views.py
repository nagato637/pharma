from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime

class HomeView(ListView):
    template_name = 'index.html'    # spécifie le template à utiliser
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()

class AddProduct(CreateView):
    model = Product
    template_name = 'adding.html'
    form_class = AddProductForm
    success_url = reverse_lazy('index')

# class UpdateProduct(UpdateView):
#     model = Product
#     template_name = 'updating.html'
#     form_class = UpdateProductForm
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         messages.success(self.request, "Produit mis à jour avec succès.")
#         return super().form_valid(form)