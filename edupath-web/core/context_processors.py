"""
Core Context Processors - Global template context from database.

Consolidates all context processors into a single cached function to avoid
running ~15 separate database queries on every request.
"""

from django.core.cache import cache
from django.db.models import Count, Q


CONTEXT_CACHE_KEY = 'global_template_context'
CONTEXT_CACHE_TIMEOUT = 300  # 5 minutes


def _build_global_context():
    """Build the full global context from database (called on cache miss)."""
    from .models import (
        BusinessPartner, Feature, SiteStatistic, PricingPlan,
        ContactInfo, SiteConfiguration,
    )
    from courses.models import Course, Instructor, Category, Review
    from blog.models import Blog

    # Site config (singleton)
    try:
        config = SiteConfiguration.get_solo()
        site_context = {
            'site_name': config.site_name,
            'site_config': config,
            'copyright_year': config.copyright_text or '2024',
        }
    except Exception:
        site_context = {
            'site_name': 'EduPath',
            'site_config': None,
            'copyright_year': '2024',
        }

    # Bulk queries
    business = list(BusinessPartner.objects.filter(is_active=True))
    features = list(Feature.objects.filter(is_active=True))
    ctas = list(SiteStatistic.objects.filter(is_active=True))
    pages = list(PricingPlan.objects.filter(is_active=True))
    contacts = list(ContactInfo.objects.filter(is_active=True))

    courses_qs = Course.objects.filter(is_active=True).select_related('category', 'instructor')
    courses = list(courses_qs)
    instructors = list(Instructor.objects.filter(is_active=True))
    categories = list(Category.objects.filter(is_active=True).annotate(
        course_count=Count('courses', filter=Q(courses__is_active=True))
    ))
    reviews = list(Review.objects.filter(is_active=True))
    blogs = list(Blog.objects.filter(is_active=True).select_related('author'))

    courses1 = [c for c in courses if c.video_url]
    courses2 = [c for c in courses if c.video_file]
    courses3 = [c for c in courses if c.is_featured][:3]

    ctx = {
        **site_context,
        'business': business,
        'features': features,
        'ctas': ctas,
        'pages': pages,
        'contacts': contacts,
        'courses': courses,
        'instructors': instructors,
        'categories': categories,
        'reviews': reviews,
        'blogs': blogs,
        'courses1': courses1,
        'courses2': courses2,
        'courses3': courses3,
    }
    return ctx


def global_context(request):
    """
    Single cached context processor replacing 15 individual ones.

    Caches database results for CONTEXT_CACHE_TIMEOUT seconds, with per-request
    additions for selected_course/selected_blog and user info.
    """
    ctx = cache.get(CONTEXT_CACHE_KEY)
    if ctx is None:
        ctx = _build_global_context()
        cache.set(CONTEXT_CACHE_KEY, ctx, CONTEXT_CACHE_TIMEOUT)

    # Per-request additions (not cached)
    result = dict(ctx)

    course_id = request.GET.get('course_id')
    if course_id:
        try:
            course_id = int(course_id)
            result['selected_course'] = next(
                (c for c in result['courses'] if c.id == course_id), None
            )
        except (TypeError, ValueError):
            result['selected_course'] = None
    else:
        result['selected_course'] = None

    blog_id = request.GET.get('blog_id')
    if blog_id:
        try:
            blog_id = int(blog_id)
            result['selected_blog'] = next(
                (b for b in result['blogs'] if b.id == blog_id), None
            )
        except (TypeError, ValueError):
            result['selected_blog'] = None
    else:
        result['selected_blog'] = None

    return result


def user_info(request):
    """User-related information if authenticated."""
    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        return {
            'user_full_name': full_name or request.user.username,
            'user_email': request.user.email,
        }
    return {}
