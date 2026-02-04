"""
URL configuration for Edupath project.

Multi-app architecture with dual-layer pattern:
- Frontend views: Server-rendered HTML templates
- API views: REST API endpoints (DRF)

URL Structure:
- /admin/ - Django admin
- /accounts/ - Authentication (django-allauth) + user profiles
- /courses/ - Courses, categories, instructors, reviews
- /blog/ - Blog posts
- / - Core app (static pages, contact, homepage API)

API Namespace: /app/api/v1/resource/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from App import views as legacy_views


urlpatterns = [
    # ==========================================================================
    # ADMIN
    # ==========================================================================
    path('admin/', admin.site.urls),

    # ==========================================================================
    # AUTHENTICATION (django-allauth + custom accounts)
    # ==========================================================================
    path('accounts/', include('accounts.urls')),

    # ==========================================================================
    # COURSES APP (categories, instructors, courses, reviews)
    # ==========================================================================
    path('courses/', include('courses.urls')),

    # ==========================================================================
    # BLOG APP
    # ==========================================================================
    path('blog/', include('blog.urls')),

    # ==========================================================================
    # CORE APP (static pages, contact, site config)
    # ==========================================================================
    path('core/', include('core.urls')),

    # ==========================================================================
    # LEGACY APP ROUTES (for backward compatibility with existing templates)
    # ==========================================================================
    # Homepage
    path('', legacy_views.index, name='index'),

    # Development tools
    path('__reload__/', include('django_browser_reload.urls')),
]

# =============================================================================
# MEDIA FILES (Development only)
# =============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
