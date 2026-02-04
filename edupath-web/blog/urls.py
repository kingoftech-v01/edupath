"""
Blog URLs - Blog listing and detail URLs.

URL Namespaces:
- Frontend: blog:view_name
- API: blog:api:resource-name
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER
# =============================================================================

api_router = DefaultRouter()
api_router.register(r'posts', views_api.BlogViewSet, basename='post')

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
    # Blog listings
    path('', views_frontend.blog_list, name='blog_list'),
    path('sidebar/', views_frontend.blog_sidebar, name='blog_sidebar'),

    # Blog detail
    path('<slug:slug>/', views_frontend.blog_detail, name='blog_detail'),
    path('detail/<int:blog_id>/', views_frontend.blog_detail_by_id, name='blog_detail_by_id'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'blog'

urlpatterns = [
    # API URLs
    path('api/v1/', include((api_urlpatterns, 'api'))),

    # Frontend URLs
    path('', include(frontend_urlpatterns)),
]
