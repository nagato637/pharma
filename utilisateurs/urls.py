from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'utilisateurs'

urlpatterns = [
    path('logout', views.disconnect, name='logout'),                      # lien deconnexion
    path('login/', views.signin, name='login'),                           # page de connexion
    path('register/', views.signup, name='register'),                     # page d'inscription
    # path('confirm-email', as_view(), name='confirm-email'),               # confirmer email
    path('reset-password', views.reset_password, name='reset-password'),             # initialiser mot de passe
    path('check-mail', views.check_mail, name='check-mail'),             # initialiser mot de passe
    # path('change-password', as_view(), name='change-passwor'),            # changer mot de passe

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)          # pour afficher les images dans le navigateur
