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
    """
    About us page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered about us template.
    """
    return render(request, 'pages/aboutus.html')


def features(request):
    """
    Features page.

    Displays platform features from context processor.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered features template.
    """
    return render(request, 'pages/features.html')


def pricing(request):
    """
    Pricing page.

    Displays pricing plans from context processor.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered pricing template.
    """
    return render(request, 'pages/pricing.html')


def faqs(request):
    """
    FAQs page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered FAQs template.
    """
    return render(request, 'pages/faqs.html')


def terms(request):
    """
    Terms of service page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered terms template.
    """
    return render(request, 'pages/terms.html')


def privacy(request):
    """
    Privacy policy page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered privacy policy template.
    """
    return render(request, 'pages/privacy.html')


# =============================================================================
# CONTACT
# =============================================================================

def contactus(request):
    """
    Contact page with form handling.

    GET: Displays empty contact form.
    POST: Validates and saves contact submission.

    Links submission to user account if logged in.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered contact template or redirect on success.
    """
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
    """
    Coming soon page.

    Placeholder for features under development.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered coming soon template.
    """
    return render(request, 'pages/comingsoon.html')


def maintenance(request):
    """
    Maintenance page.

    Shown when site is under maintenance.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered maintenance template.
    """
    return render(request, 'pages/maintenance.html')


def notFound(request):
    """
    404 page.

    Custom 404 error page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered 404 template.
    """
    return render(request, 'pages/404.html')
