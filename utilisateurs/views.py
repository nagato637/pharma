from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
        form = UserCreationForm()

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UserCreationForm()
    return render(request, 'register.html', { 'form': form })
