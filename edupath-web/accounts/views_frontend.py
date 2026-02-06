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
    """
    User profile display page.

    Renders the user's profile information. Requires authentication.
    Profile data is accessible via request.user.profile in the template.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered profile template.
    """
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    """
    User profile edit page.

    Handles both GET (display form) and POST (save changes) requests.
    Updates both UserProfile and User model fields (first_name, last_name).

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered edit form or redirect to profile on success.
    """
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
    """
    Login page - renders custom template with allauth.

    Redirects already-authenticated users to homepage.
    The actual authentication is handled by django-allauth.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirect if authenticated, otherwise login template.
    """
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'pages/login.html')


def signup_view(request):
    """
    Signup page - renders custom template with allauth.

    Redirects already-authenticated users to homepage.
    The actual registration is handled by django-allauth.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirect if authenticated, otherwise signup template.
    """
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'pages/signup.html')


def logout_view(request):
    """
    Logout and redirect to homepage.

    Ends the user's session and displays a confirmation message.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to homepage.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


def password_reset_view(request):
    """
    Password reset page.

    Renders the password reset request form.
    Actual reset logic is handled by django-allauth.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered password reset template.
    """
    return render(request, 'pages/forgot-password.html')
