"""
Core Context Processors - Global template context from database.

Provides global template context using database models.
Maintains the same variable names for template compatibility.
"""

from django.db.models import Count, Q


def global_business_data(request):
    """
    Business partner logos from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'business' queryset.
    """
    from .models import BusinessPartner
    business = BusinessPartner.objects.filter(is_active=True)
    return {'business': business}


def global_features(request):
    """
    Platform features from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'features' queryset.
    """
    from .models import Feature
    features = Feature.objects.filter(is_active=True)
    return {'features': features}


def global_ctas(request):
    """
    Site statistics from database (CTA counters).

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'ctas' queryset.
    """
    from .models import SiteStatistic
    ctas = SiteStatistic.objects.filter(is_active=True)
    return {'ctas': ctas}


def global_pages(request):
    """
    Pricing plans from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'pages' queryset.
    """
    from .models import PricingPlan
    pages = PricingPlan.objects.filter(is_active=True)
    return {'pages': pages}


def global_contacts(request):
    """
    Contact information from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'contacts' queryset.
    """
    from .models import ContactInfo
    contacts = ContactInfo.objects.filter(is_active=True)
    return {'contacts': contacts}


def site_config(request):
    """
    Site-wide configuration from database.

    Provides site name, config object, and copyright year.
    Falls back to defaults if database is unavailable.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with site configuration values.
    """
    from .models import SiteConfiguration
    try:
        config = SiteConfiguration.get_solo()
        return {
            'site_name': config.site_name,
            'site_config': config,
            'copyright_year': config.copyright_text or '2024',
        }
    except Exception:
        # Fallback ensures templates render even if DB is unreachable or migrations pending.
        return {
            'site_name': 'EduPath',
            'site_config': None,
            'copyright_year': '2024',
        }


def global_courses(request):
    """
    Courses from database with optional selected course for highlighting.

    Supports ?course_id=X query param to highlight a specific course.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'courses' queryset and optional 'selected_course'.
    """
    from courses.models import Course
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')

    # Templates can pass ?course_id=X to highlight a specific course in listings.
    course_id = request.GET.get('course_id')
    selected_course = None

    if course_id:
        try:
            course_id = int(course_id)
            selected_course = courses.filter(id=course_id).first()
        except (TypeError, ValueError):
            # Silently ignore invalid IDs - just won't highlight any course.
            selected_course = None

    return {'courses': courses, 'selected_course': selected_course}


def global_instructors(request):
    """
    Instructors from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'instructors' queryset.
    """
    from courses.models import Instructor
    instructors = Instructor.objects.filter(is_active=True)
    return {'instructors': instructors}


def global_categories(request):
    """
    Categories from database with course counts.

    Annotates each category with active course count to avoid N+1.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'categories' queryset.
    """
    from courses.models import Category
    # Annotate counts in DB to avoid N+1 queries. Only count active courses,
    # not soft-deleted ones, so UI shows accurate "X courses" labels.
    categories = Category.objects.filter(is_active=True).annotate(
        course_count=Count('courses', filter=Q(courses__is_active=True))
    )
    return {'categories': categories}


def global_reviews(request):
    """
    Reviews from database.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'reviews' queryset.
    """
    from courses.models import Review
    reviews = Review.objects.filter(is_active=True)
    return {'reviews': reviews}


def global_blogs(request):
    """
    Blogs from database with selected blog handling.

    Supports ?blog_id=X query param to highlight a specific blog.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'blogs' queryset and optional 'selected_blog'.
    """
    from blog.models import Blog
    blogs = Blog.objects.filter(is_active=True).select_related('author')

    blog_id = request.GET.get('blog_id')
    selected_blog = None

    if blog_id:
        try:
            blog_id = int(blog_id)
            selected_blog = blogs.filter(id=blog_id).first()
        except (TypeError, ValueError):
            selected_blog = None

    return {'blogs': blogs, 'selected_blog': selected_blog}


def global_courses1(request):
    """
    Courses with YouTube embeds (video_url field).

    Returns courses with non-empty video_url for YouTube player.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'courses1' queryset.
    """
    from courses.models import Course
    # courses1 = YouTube embeds, courses2 = self-hosted videos.
    # Split allows templates to use different players for each type.
    courses1 = Course.objects.filter(
        is_active=True,
    ).exclude(video_url='').exclude(video_url__isnull=True).select_related('instructor')
    return {'courses1': courses1}


def global_courses2(request):
    """
    Courses with self-hosted videos (video_file field).

    Returns courses with uploaded video files for HTML5 player.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'courses2' queryset.
    """
    from courses.models import Course
    courses2 = Course.objects.filter(
        is_active=True,
        video_file__isnull=False
    ).exclude(video_file='').select_related('instructor')
    return {'courses2': courses2}


def global_courses3(request):
    """
    Featured courses subset from database (3 courses).

    Returns up to 3 featured courses for sidebar/widget display.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with 'courses3' queryset.
    """
    from courses.models import Course
    courses3 = Course.objects.filter(is_active=True, is_featured=True)[:3]
    return {'courses3': courses3}


def user_info(request):
    """
    User-related information if authenticated.

    Provides full name and email for authenticated users.

    Args:
        request: The HTTP request object.

    Returns:
        dict: Context with user info or empty dict if anonymous.
    """
    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        return {
            'user_full_name': full_name or request.user.username,
            'user_email': request.user.email,
        }
    return {}
