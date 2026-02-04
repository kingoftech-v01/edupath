"""
Core Frontend Views - Static pages and contact views.
"""

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm


# =============================================================================
# STATIC PAGES
# =============================================================================

def aboutus(request):
    """About us page."""
    return render(request, 'pages/aboutus.html')


def features(request):
    """Features page."""
    return render(request, 'pages/features.html')


def pricing(request):
    """Pricing page."""
    return render(request, 'pages/pricing.html')


def faqs(request):
    """FAQs page."""
    return render(request, 'pages/faqs.html')


def terms(request):
    """Terms of service page."""
    return render(request, 'pages/terms.html')


def privacy(request):
    """Privacy policy page."""
    return render(request, 'pages/privacy.html')


# =============================================================================
# CONTACT
# =============================================================================

def contactus(request):
    """Contact page with form handling."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            if request.user.is_authenticated:
                submission.user = request.user
            submission.save()
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('core:contactus')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'pages/contactus.html', {'form': form})


# =============================================================================
# UTILITY PAGES
# =============================================================================

def comingsoon(request):
    """Coming soon page."""
    return render(request, 'pages/comingsoon.html')


def maintenance(request):
    """Maintenance page."""
    return render(request, 'pages/maintenance.html')


def notFound(request):
    """404 page."""
    return render(request, 'pages/404.html')
