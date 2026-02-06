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
    """
    Course list/grid page with optional filtering.

    Supports filtering by category, search term, and price type.
    Results are paginated (12 per page for 3-column grid).

    Query params:
        category: Filter by category slug.
        search: Search in title and description.
        price: Filter by 'free' or 'paid'.
        page: Pagination page number.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered course grid template.
    """
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
    """
    Course grid listing.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered grid template.
    """
    return render(request, 'pages/grid.html')


def grid_sidebar(request):
    """
    Course grid with sidebar layout.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered grid-sidebar template.
    """
    return render(request, 'pages/grid-sidebar.html')


def list_view(request):
    """
    Course list view (rows instead of grid).

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered list template.
    """
    return render(request, 'pages/list.html')


def list_sidebar(request):
    """
    Course list with sidebar layout.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered list-sidebar template.
    """
    return render(request, 'pages/list-sidebar.html')


def youtube_listing(request):
    """
    YouTube video courses listing.

    Shows courses with YouTube embeds (video_url field).

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered YouTube listing template.
    """
    return render(request, 'pages/youtube-listing.html')


def video_listing(request):
    """
    Self-hosted video courses listing.

    Shows courses with uploaded videos (video_file field).

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered video listing template.
    """
    return render(request, 'pages/video-listing.html')


# =============================================================================
# COURSE DETAIL VIEWS
# =============================================================================

def course_detail(request, slug):
    """
    Course detail page by slug.

    Displays full course information with related courses and reviews.
    Shows review form for authenticated users.

    Args:
        request: The HTTP request object.
        slug: Course URL slug.

    Returns:
        HttpResponse: Rendered course detail template.
    """
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
    """
    Course detail page by ID.

    Maintains backward compatibility with old numeric ID URLs.

    Args:
        request: The HTTP request object.
        course_id: Numeric course ID.

    Returns:
        HttpResponse: Rendered course detail template.
    """
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
    """
    Alternative course detail page layout.

    Uses a different template design for A/B testing or variety.

    Args:
        request: The HTTP request object.
        course_id: Numeric course ID.

    Returns:
        HttpResponse: Rendered alternative course detail template.
    """
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
    """
    Instructor listing page.

    Shows all active instructors with their profiles.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered instructors template.
    """
    return render(request, 'pages/instructors.html')


def instructor_detail(request, slug):
    """
    Instructor detail page.

    Shows instructor profile and their courses.

    Args:
        request: The HTTP request object.
        slug: Instructor URL slug.

    Returns:
        HttpResponse: Rendered instructor detail template.
    """
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
    """
    Category listing page.

    Shows all active categories with their course counts.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered category list template.
    """
    categories = Category.objects.filter(is_active=True)
    return render(request, 'courses/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """
    Category detail page with courses.

    Shows category info and paginated list of courses in that category.

    Args:
        request: The HTTP request object.
        slug: Category URL slug.

    Returns:
        HttpResponse: Rendered category detail template.
    """
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
    """
    HTMX partial for filtered course listings on homepage.

    Returns HTML fragment for HTMX swap without full page reload.
    Supports category and search filtering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered course list partial (max 12 courses).
    """
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
    """
    HTMX endpoint for submitting reviews without page reload.

    Creates a new review for the specified course.
    Auto-populates user and name from authenticated session.

    Args:
        request: The HTTP request object (POST only).
        course_id: Numeric course ID.

    Returns:
        JsonResponse: Success message or validation errors.
    """
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
