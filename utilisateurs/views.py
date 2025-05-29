from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

# fonction connexion
def signin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'username or password incorrect')
            return redirect('utilisateurs:login')
        
    form = AuthenticationForm()
    return render(request, 'login.html', { 'form': form })

def disconnect(request):
    logout(request)
    return redirect('home')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # vérification mot de passe
        if password != password_confirm:
            messages.error(request, 'passwords are different')
            return redirect('utilisateurs:register')

        # vérification si mot de passe contains special character
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*()":;<>,.?/]', password):
            messages.error(request, 'password must contain 8 characters, letters and numbers and special characters')
            return redirect('utilisateurs:register')
        
        # vérification et validation de l'email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'invalid email')
            return redirect('utilisateurs:register')
        
        # vérification de l'user et email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user already exists')
            return redirect('utilisateurs:register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return redirect('utilisateurs:register')
        
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'user is created')
        
        return redirect('utilisateurs:login')
    
    return render(request, 'register.html')

def check_mail(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'email is required')
            return redirect('')
        
        user = User.objects.filter(email=email).first()

        if user:
            return redirect('utilisateurs:reset-password', email=email)
        else:
            messages.error(request, 'email not found')
            return redirect('')
        
    return render(request, 'checkmail.html')

def reset_password(request, email):
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        messages.error(request, 'user not found')
        return redirect('utilisateurs:check-mail')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:

            if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*()":;<>,.?/]', password):
                messages.error(request, 'password must contain 8 characters, letters and numbers and special characters')
            
        else:
            user.set_password(password)
            user.save()
            messages.success(request, 'password changed successfully')
            return redirect('utilisateurs:login')
        
    else:
        messages.error(request, 'passwords are different')

    return render(request, 'reset_password.html', {'email': email})
