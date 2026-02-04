"""
Courses URLs - Course, Category, Instructor URLs.

URL Namespaces:
- Frontend: courses:view_name
- API: courses:api:resource-name
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER
# =============================================================================

api_router = DefaultRouter()
api_router.register(r'categories', views_api.CategoryViewSet, basename='category')
api_router.register(r'instructors', views_api.InstructorViewSet, basename='instructor')
api_router.register(r'courses', views_api.CourseViewSet, basename='course')
api_router.register(r'reviews', views_api.ReviewViewSet, basename='review')

# =============================================================================
# API URLPATTERNS
# =============================================================================

api_urlpatterns = [
    path('', include(api_router.urls)),
]

# =============================================================================
# FRONTEND URLPATTERNS
# =============================================================================

frontend_urlpatterns = [
    # Course listings
    path('', views_frontend.course_list, name='course_list'),
    path('grid/', views_frontend.grid, name='grid'),
    path('grid-sidebar/', views_frontend.grid_sidebar, name='grid_sidebar'),
    path('list/', views_frontend.list_view, name='list'),
    path('list-sidebar/', views_frontend.list_sidebar, name='list_sidebar'),
    path('youtube/', views_frontend.youtube_listing, name='youtube_listing'),
    path('video/', views_frontend.video_listing, name='video_listing'),

    # Instructors (must be before slug pattern)
    path('instructors/', views_frontend.instructor_list, name='instructor_list'),
    path('instructors/<slug:slug>/', views_frontend.instructor_detail, name='instructor_detail'),

    # Categories (must be before slug pattern)
    path('categories/', views_frontend.category_list, name='category_list'),
    path('categories/<slug:slug>/', views_frontend.category_detail, name='category_detail'),

    # HTMX partials
    path('htmx/course-list/', views_frontend.htmx_course_list, name='htmx_course_list'),
    path('htmx/review/<int:course_id>/', views_frontend.htmx_submit_review, name='htmx_submit_review'),

    # Course detail (slug pattern must be last to avoid catching other paths)
    path('detail/<int:course_id>/', views_frontend.course_detail_by_id, name='course_detail_by_id'),
    path('detail-two/<int:course_id>/', views_frontend.course_detail_two, name='course_detail_two'),
    path('<slug:slug>/', views_frontend.course_detail, name='course_detail'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'courses'

urlpatterns = [
    # API URLs
    path('api/v1/', include((api_urlpatterns, 'api'))),

    # Frontend URLs
    path('', include(frontend_urlpatterns)),
]
