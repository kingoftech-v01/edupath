"""
Courses Frontend Views - Course listing and detail views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Category, Instructor, Course, Review
from .forms import ReviewForm


# =============================================================================
# COURSE LISTING VIEWS
# =============================================================================

def course_list(request):
    """Course list/grid page with optional filtering."""
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')

    # Filter chain: all filters are optional and can combine.
    # URL examples: ?category=web-dev&price=free&search=python
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

    # 12 per page fits the 3-column grid layout (4 rows).
    paginator = Paginator(courses, 12)
    page = request.GET.get('page', 1)
    courses_page = paginator.get_page(page)

    context = {
        'courses': courses_page,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'pages/grid.html', context)


def grid(request):
    """Course grid listing."""
    return render(request, 'pages/grid.html')


def grid_sidebar(request):
    """Course grid with sidebar."""
    return render(request, 'pages/grid-sidebar.html')


def list_view(request):
    """Course list view."""
    return render(request, 'pages/list.html')


def list_sidebar(request):
    """Course list with sidebar."""
    return render(request, 'pages/list-sidebar.html')


def youtube_listing(request):
    """YouTube video courses."""
    return render(request, 'pages/youtube-listing.html')


def video_listing(request):
    """Video courses listing."""
    return render(request, 'pages/video-listing.html')


# =============================================================================
# COURSE DETAIL VIEWS
# =============================================================================

def course_detail(request, slug):
    """Course detail page by slug."""
    course = get_object_or_404(
        Course.objects.select_related('category', 'instructor'),
        slug=slug,
        is_active=True
    )

    related_courses = Course.objects.filter(
        is_active=True
    ).exclude(pk=course.pk)[:3]

    reviews = course.reviews.filter(is_active=True)

    context = {
        'course': course,
        'selected_course': course,
        'courses3': related_courses,
        'course_reviews': reviews,
        'review_form': ReviewForm() if request.user.is_authenticated else None,
    }
    return render(request, 'pages/course-detail.html', context)


def course_detail_by_id(request, course_id):
    """Course detail page by ID (for legacy URLs)."""
    course = get_object_or_404(
        Course.objects.select_related('category', 'instructor'),
        id=course_id,
        is_active=True
    )

    related_courses = Course.objects.filter(is_active=True).exclude(pk=course.pk)[:3]
    reviews = course.reviews.filter(is_active=True)

    context = {
        'course': course,
        'selected_course': course,
        'courses3': related_courses,
        'course_reviews': reviews,
    }
    return render(request, 'pages/course-detail.html', context)


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
# INSTRUCTOR VIEWS
# =============================================================================

def instructor_list(request):
    """Instructor listing page."""
    return render(request, 'pages/instructors.html')


def instructor_detail(request, slug):
    """Instructor detail page."""
    instructor = get_object_or_404(Instructor, slug=slug, is_active=True)
    courses = instructor.courses.filter(is_active=True)

    context = {
        'instructor': instructor,
        'courses': courses,
    }
    return render(request, 'courses/instructor_detail.html', context)


# =============================================================================
# CATEGORY VIEWS
# =============================================================================

def category_list(request):
    """Category listing page."""
    categories = Category.objects.filter(is_active=True)
    return render(request, 'courses/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """Category detail with courses."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    courses = category.courses.filter(is_active=True)

    # Pagination
    paginator = Paginator(courses, 12)
    page = request.GET.get('page', 1)
    courses_page = paginator.get_page(page)

    context = {
        'category': category,
        'courses': courses_page,
    }
    return render(request, 'courses/category_detail.html', context)


# =============================================================================
# HTMX VIEWS
# =============================================================================
# These views return HTML partials for HTMX-powered dynamic updates without
# full page reloads. They're called via hx-get/hx-post attributes in templates.

def htmx_course_list(request):
    """HTMX partial for filtered course listings on homepage."""
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')

    category = request.GET.get('category')
    if category:
        courses = courses.filter(category__slug=category)

    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) |
            Q(desc__icontains=search)
        )

    # Limit 12 matches homepage course grid; no pagination for partial refresh.
    context = {'courses': courses[:12]}
    return render(request, 'Components/home/courses.html', context)


@login_required
@require_POST
def htmx_submit_review(request, course_id):
    """HTMX endpoint for submitting reviews without page reload."""
    course = get_object_or_404(Course, id=course_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        # Auto-set course from URL and user from session - prevents tampering.
        review.course = course
        review.user = request.user
        review.name = request.user.get_full_name() or request.user.username
        review.save()

        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully!'
        })

    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)
