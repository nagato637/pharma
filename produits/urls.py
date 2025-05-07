from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'), # Page d'accueil
    path('', HomeView.as_view(), name='product'),                           # Liste des produits
    path('add/', views.addProduct, name='add'),                             # Ajouter un produit

] + static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)         # Pour afficher les images dans le navigateur
