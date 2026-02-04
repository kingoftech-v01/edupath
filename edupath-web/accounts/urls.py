"""
Accounts URLs - Authentication and profile URLs.

Uses django-allauth for authentication endpoints.
Frontend URLs follow URL_AND_VIEW_CONVENTIONS.md

URL Namespaces:
- Frontend: accounts:view_name
- API: accounts:api:resource-name
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER
# =============================================================================

api_router = DefaultRouter()
api_router.register(r'profiles', views_api.UserProfileViewSet, basename='profile')

# =============================================================================
# API URLPATTERNS
# =============================================================================

api_urlpatterns = [
    path('', include(api_router.urls)),
    path('me/', views_api.CurrentUserAPIView.as_view(), name='current-user'),
]

# =============================================================================
# FRONTEND URLPATTERNS
# =============================================================================

frontend_urlpatterns = [
    # Profile views
    path('profile/', views_frontend.profile_view, name='profile'),
    path('profile/edit/', views_frontend.profile_edit, name='profile_edit'),

    # Override allauth templates with custom views if needed
    path('login/', views_frontend.login_view, name='login'),
    path('signup/', views_frontend.signup_view, name='signup'),
    path('logout/', views_frontend.logout_view, name='logout'),
    path('password/reset/', views_frontend.password_reset_view, name='password_reset'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'accounts'

urlpatterns = [
    # API URLs: /accounts/api/v1/
    path('api/v1/', include((api_urlpatterns, 'api'))),

    # Frontend URLs: /accounts/
    path('', include(frontend_urlpatterns)),

    # Allauth URLs
    path('', include('allauth.urls')),
]
