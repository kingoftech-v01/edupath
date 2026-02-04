"""
Accounts Frontend Views - Profile and authentication views.

Uses django-allauth for authentication.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm


# =============================================================================
# PROFILE VIEWS
# =============================================================================

@login_required
def profile_view(request):
    """User profile display page."""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    """User profile edit page."""
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # Update User model fields
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form})


# =============================================================================
# AUTHENTICATION VIEWS (Wrappers for allauth)
# =============================================================================

def login_view(request):
    """Login page - renders custom template with allauth."""
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'pages/login.html')


def signup_view(request):
    """Signup page - renders custom template with allauth."""
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'pages/signup.html')


def logout_view(request):
    """Logout and redirect."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


def password_reset_view(request):
    """Password reset page."""
    return render(request, 'pages/forgot-password.html')
