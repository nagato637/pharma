from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'produits'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),                             # page d'accueil
    path('add/', AddProduct.as_view(), name='add'),                         # ajouter un produit
    path('search/', views.search, name='search'),                           # chercher un produit
    path('update/<int:pk>/', UpdateProduct.as_view(), name='update'),       # mettre à jour un produit
    path('delete/<int:pk>/', DeleteProduct.as_view(), name='delete'),       # supprimer un produit
    path('show/<int:pk>/', ShowProduct.as_view(), name='show'),             # afficher un produit

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)          # pour afficher les images dans le navigateur
