from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Perform form validation
        if not username or not email or not password:
            return render(request, 'Accounts/signup.html', {'error': 'All fields are required'})

        # Create a new user profile and hash the password
        user = UserProfile(username=username, email=email)
        user.set_password(password)  # Hash the password
        user.save()

        return redirect('login')  # Redirect to login page after successful signup
    return render(request, 'Accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard URL
        else:
            return render(request, 'Accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'Accounts/login.html')

def dashboard_view(request):
    # Implement your dashboard view logic here
    return render(request, 'dashboard.html')