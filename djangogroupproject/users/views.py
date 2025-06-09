from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
from .models import Profile
import uuid

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('users:login')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('campaigns:list')

@login_required
def profile(request):
    """User profile view"""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
    
    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def change_role(request):
    """Change user role view"""
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in dict(Profile.ROLE_CHOICES):
            profile = request.user.profile
            profile.role = new_role
            profile.save()
            messages.success(request, f'Your role has been changed to {new_role}.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Invalid role selection.')
    
    return redirect('users:profile')

@login_required
def delete_account(request):
    """Delete user account view"""
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('campaigns:list')
    
    return render(request, 'users/delete_account.html')
