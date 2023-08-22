from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Use dashboard_view here
    # Add other URLs as needed
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),

    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

]
