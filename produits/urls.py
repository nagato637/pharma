from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'), # Page d'accueil
    path('', HomeView.as_view(), name='index'),                             # liste des produits
    path('add/', AddProduct.as_view(), name='add'),                         # ajouter un produit
    # path('update/<int:id>/', views.update, name='update'),                 # modifier un produit
    path('update/<int:pk>/', UpdateProduct.as_view(), name='update'),       # mettre à jour un produit
    # path('delete/<int:id>/', views.delete, name='delete'),                 # supprimer un produit
    # path('show/<int:id>/', views.show, name='show'),                       # afficher un produit
    path('show/<int:pk>/', ShowProduct.as_view(), name='show'),             # afficher un produit

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)         # pour afficher les images dans le navigateur
