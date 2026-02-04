"""
Core Context Processors - Global template context from database.

Provides global template context using database models.
Maintains the same variable names for template compatibility.
"""

from django.db.models import Count, Q


def global_business_data(request):
    """Business partner logos from database."""
    from .models import BusinessPartner
    business = BusinessPartner.objects.filter(is_active=True)
    return {'business': business}


def global_features(request):
    """Platform features from database."""
    from .models import Feature
    features = Feature.objects.filter(is_active=True)
    return {'features': features}


def global_ctas(request):
    """Site statistics from database (CTA counters)."""
    from .models import SiteStatistic
    ctas = SiteStatistic.objects.filter(is_active=True)
    return {'ctas': ctas}


def global_pages(request):
    """Pricing plans from database."""
    from .models import PricingPlan
    pages = PricingPlan.objects.filter(is_active=True)
    return {'pages': pages}


def global_contacts(request):
    """Contact information from database."""
    from .models import ContactInfo
    contacts = ContactInfo.objects.filter(is_active=True)
    return {'contacts': contacts}


def site_config(request):
    """Site-wide configuration from database."""
    from .models import SiteConfiguration
    try:
        config = SiteConfiguration.get_solo()
        return {
            'site_name': config.site_name,
            'site_config': config,
            'copyright_year': config.copyright_text or '2024',
        }
    except Exception:
        return {
            'site_name': 'EduPath',
            'site_config': None,
            'copyright_year': '2024',
        }


def global_courses(request):
    """Courses from database with selected course handling."""
    from courses.models import Course
    courses = Course.objects.filter(is_active=True).select_related('category', 'instructor')

    course_id = request.GET.get('course_id')
    selected_course = None

    if course_id:
        try:
            course_id = int(course_id)
            selected_course = courses.filter(id=course_id).first()
        except (TypeError, ValueError):
            selected_course = None

    return {'courses': courses, 'selected_course': selected_course}


def global_instructors(request):
    """Instructors from database."""
    from courses.models import Instructor
    instructors = Instructor.objects.filter(is_active=True)
    return {'instructors': instructors}


def global_categories(request):
    """Categories from database with course counts."""
    from courses.models import Category
    categories = Category.objects.filter(is_active=True).annotate(
        course_count=Count('courses', filter=Q(courses__is_active=True))
    )
    return {'categories': categories}


def global_reviews(request):
    """Reviews from database."""
    from courses.models import Review
    reviews = Review.objects.filter(is_active=True)
    return {'reviews': reviews}


def global_blogs(request):
    """Blogs from database with selected blog handling."""
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
    """YouTube video courses from database."""
    from courses.models import Course
    courses1 = Course.objects.filter(
        is_active=True,
    ).exclude(video_url='').exclude(video_url__isnull=True).select_related('instructor')
    return {'courses1': courses1}


def global_courses2(request):
    """Local video courses from database."""
    from courses.models import Course
    courses2 = Course.objects.filter(
        is_active=True,
        video_file__isnull=False
    ).exclude(video_file='').select_related('instructor')
    return {'courses2': courses2}


def global_courses3(request):
    """Featured courses subset from database (3 courses)."""
    from courses.models import Course
    courses3 = Course.objects.filter(is_active=True, is_featured=True)[:3]
    return {'courses3': courses3}


def user_info(request):
    """User-related information if authenticated."""
    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        return {
            'user_full_name': full_name or request.user.username,
            'user_email': request.user.email,
        }
    return {}
