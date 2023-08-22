from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site  # Add this import
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail  # Add this import

User = get_user_model()
SITE_URL = 'http://127.0.0.1:8000'
DEFAULT_FROM_EMAIL = 'mukhos1@gmail.com'

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



def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = User.objects.filter(email=email)
            print(email, users)
            if users.exists():
                print("yes")
                user = users.first()
                
                # Generate the reset token and send the email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                current_site = get_current_site(request)
                site_url = SITE_URL  # Use the SITE_URL from settings.py
                
                reset_link = reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
                reset_url = f'{site_url}{reset_link}'
                
                email_subject = 'Password Reset'
                email_message = render_to_string('Accounts/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'site_name': current_site.name,
                })
                print(user.email)
                send_mail(email_subject, email_message, DEFAULT_FROM_EMAIL, [user.email])
                
                messages.success(request, 'An email with password reset instructions has been sent.')
                return redirect('login')
            else:
                
                messages.error(request, 'No user with that email address exists.')
    else:
        form = PasswordResetForm()
    return render(request, 'Accounts/forgot_password.html', {'form': form})

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'Accounts/reset_password.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The password reset link is no longer valid.')
        return redirect('login')
