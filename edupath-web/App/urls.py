"""
EduPath App URLs - Frontend and API routing.

URL Namespaces:
- Frontend: App:view_name
- API: App:api:resource-name

Follows URL_AND_VIEW_CONVENTIONS.md dual-layer architecture.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER (DRF ViewSets)
# =============================================================================

api_router = DefaultRouter()

# Register all ViewSets
api_router.register(r'categories', views_api.CategoryViewSet, basename='category')
api_router.register(r'instructors', views_api.InstructorViewSet, basename='instructor')
api_router.register(r'courses', views_api.CourseViewSet, basename='course')
api_router.register(r'blogs', views_api.BlogViewSet, basename='blog')
api_router.register(r'reviews', views_api.ReviewViewSet, basename='review')
api_router.register(r'features', views_api.FeatureViewSet, basename='feature')
api_router.register(r'business-partners', views_api.BusinessPartnerViewSet, basename='business-partner')
api_router.register(r'statistics', views_api.SiteStatisticViewSet, basename='statistic')
api_router.register(r'pricing-plans', views_api.PricingPlanViewSet, basename='pricing-plan')
api_router.register(r'contact-info', views_api.ContactInfoViewSet, basename='contact-info')

# =============================================================================
# API URLPATTERNS
# =============================================================================

api_urlpatterns = [
    # Router URLs (ViewSets)
    path('', include(api_router.urls)),

    # Custom API endpoints
    path('contact/', views_api.ContactSubmissionAPIView.as_view(), name='contact-submit'),
    path('site-config/', views_api.SiteConfigurationAPIView.as_view(), name='site-config'),
    path('homepage/', views_api.HomepageDataAPIView.as_view(), name='homepage-data'),
]

# =============================================================================
# FRONTEND URLPATTERNS
# =============================================================================

frontend_urlpatterns = [
    # Homepage variants
    path('', views_frontend.index, name='index'),
    path('index-two/', views_frontend.index_two, name='index_two'),
    path('index-three/', views_frontend.index_three, name='index_three'),
    path('index-four/', views_frontend.index_four, name='index_four'),
    path('index-five/', views_frontend.index_five, name='index_five'),

    # Course listings
    path('grid/', views_frontend.grid, name='grid'),
    path('grid-sidebar/', views_frontend.grid_sidebar, name='grid_sidebar'),
    path('list/', views_frontend.list_view, name='list'),
    path('list-sidebar/', views_frontend.list_sidebar, name='list_sidebar'),
    path('youtube-listing/', views_frontend.youtube_listing, name='youtube_listing'),
    path('video-listing/', views_frontend.video_listing, name='video_listing'),

    # Course detail
    path('course-detail/', views_frontend.course_list_or_default, name='course_list'),
    path('course-detail/<int:course_id>/', views_frontend.course_detail, name='course_detail'),
    path('course-detail-two/', views_frontend.course_list_or_default1, name='course_list1'),
    path('course-detail-two/<int:course_id>/', views_frontend.course_detail_two, name='course_detail_two'),

    # Static pages
    path('aboutus/', views_frontend.aboutus, name='aboutus'),
    path('features/', views_frontend.features, name='features'),
    path('pricing/', views_frontend.pricing, name='pricing'),
    path('instructors/', views_frontend.instructors, name='instructors'),
    path('faqs/', views_frontend.faqs, name='faqs'),
    path('terms/', views_frontend.terms, name='terms'),
    path('privacy/', views_frontend.privacy, name='privacy'),

    # Authentication
    path('login/', views_frontend.login_view, name='login'),
    path('signup/', views_frontend.signup_view, name='signup'),
    path('logout/', views_frontend.logout_view, name='logout'),
    path('forgot-password/', views_frontend.forgot_password, name='forgot_password'),

    # Blog
    path('blogs/', views_frontend.blogs, name='blogs'),
    path('blog-sidebar/', views_frontend.blog_sidebar, name='blog_sidebar'),
    path('blog-detail/', views_frontend.blog_list_or_default, name='blog_list'),
    path('blog-detail/<int:blog_id>/', views_frontend.blog_detail, name='blog_detail'),

    # Contact
    path('contactus/', views_frontend.contactus, name='contactus'),

    # Utility pages
    path('comingsoon/', views_frontend.comingsoon, name='comingsoon'),
    path('maintenance/', views_frontend.maintenance, name='maintenance'),
    path('404/', views_frontend.notFound, name='notFound'),

    # HTMX partials
    path('htmx/courses/', views_frontend.htmx_course_list, name='htmx_course_list'),
    path('htmx/review/<int:course_id>/', views_frontend.htmx_submit_review, name='htmx_submit_review'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'App'

urlpatterns = [
    # API URLs: /api/v1/
    path('api/v1/', include((api_urlpatterns, 'api'))),

    # Frontend URLs: /
    path('', include(frontend_urlpatterns)),
]
