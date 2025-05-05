from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Replace 'home' with your desired redirect URL name
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')  # Replace 'login.html' with your login template

def logout(request):
    auth_logout(request)
    return render(request, 'login.html')  # Replace 'login' with your desired redirect URL name