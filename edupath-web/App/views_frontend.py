"""
EduPath Frontend Views - Template rendering views with database data.

Provides HTML template views using database queries instead of
hardcoded context processors. Maintains compatibility with existing templates.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Category, Instructor, Course, Blog, Review, Feature,
    BusinessPartner, SiteStatistic, PricingPlan, ContactInfo,
    ContactSubmission, SiteConfiguration
)
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    ContactForm, ReviewForm, CourseSearchForm, PasswordResetRequestForm
)


# =============================================================================
# HOMEPAGE VIEWS
# =============================================================================

def index(request):
    """Homepage view with all dynamic content."""
    context = {
        'page_title': 'Home',
    }
    return render(request, 'pages/index.html', context)


def index_two(request):
    """Alternative homepage layout 2."""
    return render(request, 'pages/index-two.html')


def index_three(request):
    """Alternative homepage layout 3."""
    return render(request, 'pages/index-three.html')


def index_four(request):
    """Alternative homepage layout 4."""
    return render(request, 'pages/index-four.html')


def index_five(request):
    """Alternative homepage layout 5."""
    return render(request, 'pages/index-five.html')


# =============================================================================
# COURSE LISTING VIEWS
# =============================================================================

def grid(request):
    """Course grid listing."""
    return render(request, 'pages/grid.html')


def grid_sidebar(request):
    """Course grid listing with sidebar."""
    return render(request, 'pages/grid-sidebar.html')


def list_view(request):
    """Course list listing."""
    return render(request, 'pages/list.html')


def list_sidebar(request):
    """Course list listing with sidebar."""
    return render(request, 'pages/list-sidebar.html')


def youtube_listing(request):
    """YouTube video course listing."""
    return render(request, 'pages/youtube-listing.html')


def video_listing(request):
    """Video course listing."""
    return render(request, 'pages/video-listing.html')


# =============================================================================
# COURSE DETAIL VIEWS
# =============================================================================

def course_list_or_default(request):
    """Course list or detail based on query param."""
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')
    return render(request, 'pages/course-detail.html', {'courses': courses})


def course_detail(request, course_id):
    """Course detail page."""
    course = get_object_or_404(
        Course.objects.select_related('category', 'instructor'),
        id=course_id,
        is_active=True
    )

    # Related courses
    related_courses = Course.objects.filter(
        is_active=True
    ).exclude(pk=course.pk)[:3]

    # Reviews for this course
    reviews = course.reviews.filter(is_active=True)

    context = {
        'course': course,
        'selected_course': course,
        'courses3': related_courses,
        'course_reviews': reviews,
        'review_form': ReviewForm() if request.user.is_authenticated else None,
    }
    return render(request, 'pages/course-detail.html', context)


def course_list_or_default1(request):
    """Alternative course list."""
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')
    return render(request, 'pages/course-detail-two.html', {'courses': courses})


def course_detail_two(request, course_id):
    """Alternative course detail page."""
    course = get_object_or_404(
        Course.objects.select_related('category', 'instructor'),
        id=course_id,
        is_active=True
    )
    context = {
        'course': course,
        'selected_course': course,
    }
    return render(request, 'pages/course-detail-two.html', context)


# =============================================================================
# BLOG VIEWS
# =============================================================================

def blogs(request):
    """Blog listing page."""
    return render(request, 'pages/blogs.html')


def blog_sidebar(request):
    """Blog listing with sidebar."""
    return render(request, 'pages/blog-sidebar.html')


def blog_list_or_default(request):
    """Blog list or detail."""
    blogs_list = Blog.objects.filter(is_active=True).select_related('author')
    return render(request, 'pages/blog-detail.html', {'blogs': blogs_list})


def blog_detail(request, blog_id):
    """Blog detail page."""
    blog = get_object_or_404(Blog, id=blog_id, is_active=True)

    # Recent blogs for sidebar
    recent_blogs = Blog.objects.filter(is_active=True).exclude(pk=blog.pk)[:5]

    context = {
        'blog': blog,
        'selected_blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'pages/blog-detail.html', context)


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


def instructors(request):
    """Instructors listing page."""
    return render(request, 'pages/instructors.html')


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
# CONTACT VIEWS
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
            return redirect('App:contactus')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/contactus.html', context)


# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

def login_view(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('App:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle remember me
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            next_url = request.GET.get('next', 'App:index')
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})


def signup_view(request):
    """Registration page."""
    if request.user.is_authenticated:
        return redirect('App:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to EduPath.')
            return redirect('App:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'pages/signup.html', {'form': form})


def logout_view(request):
    """Logout handler."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('App:index')


def forgot_password(request):
    """Password reset request page."""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # TODO: Implement actual email sending
            messages.success(
                request,
                'If an account exists with that email, you will receive a password reset link.'
            )
            return redirect('App:login')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'pages/forgot-password.html', {'form': form})


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


# =============================================================================
# HTMX PARTIAL VIEWS (for dynamic updates without full page reload)
# =============================================================================

def htmx_course_list(request):
    """HTMX partial for filtered course listings."""
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')

    # Apply filters
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category__slug=category)

    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) |
            Q(desc__icontains=search)
        )

    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)

    context = {'courses': courses[:12]}
    return render(request, 'Components/home/courses.html', context)


@login_required
@require_POST
def htmx_submit_review(request, course_id):
    """HTMX endpoint for submitting course reviews."""
    course = get_object_or_404(Course, id=course_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.course = course
        review.user = request.user
        review.name = request.user.get_full_name() or request.user.username
        review.save()

        # Return success message or updated reviews list
        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully!'
        })

    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)
