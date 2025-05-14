from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect based on user role
            if user.is_superuser:
                return redirect('/owner/dashboard')  # Redirect superusers to the owner dashboard
            else:
                return redirect('/exec/dashboard')  # Redirect executives to the executive dashboard
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')  # Render the login page

def logout(request):
    auth_logout(request)
    return render(request, 'login.html')  # Render the login page after logout