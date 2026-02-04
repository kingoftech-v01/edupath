"""
Core URLs - Static pages, contact, pricing URLs.

URL Namespaces:
- Frontend: core:view_name
- API: core:api:resource-name
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER
# =============================================================================

api_router = DefaultRouter()
api_router.register(r'features', views_api.FeatureViewSet, basename='feature')
api_router.register(r'business-partners', views_api.BusinessPartnerViewSet, basename='business-partner')
api_router.register(r'statistics', views_api.SiteStatisticViewSet, basename='statistic')
api_router.register(r'pricing-plans', views_api.PricingPlanViewSet, basename='pricing-plan')
api_router.register(r'contact-info', views_api.ContactInfoViewSet, basename='contact-info')

# =============================================================================
# API URLPATTERNS
# =============================================================================

api_urlpatterns = [
    path('', include(api_router.urls)),
    path('contact/', views_api.ContactSubmissionAPIView.as_view(), name='contact-submit'),
    path('site-config/', views_api.SiteConfigurationAPIView.as_view(), name='site-config'),
    path('homepage/', views_api.HomepageDataAPIView.as_view(), name='homepage-data'),
]

# =============================================================================
# FRONTEND URLPATTERNS
# =============================================================================

frontend_urlpatterns = [
    # Static pages
    path('about/', views_frontend.aboutus, name='aboutus'),
    path('features/', views_frontend.features, name='features'),
    path('pricing/', views_frontend.pricing, name='pricing'),
    path('faqs/', views_frontend.faqs, name='faqs'),
    path('terms/', views_frontend.terms, name='terms'),
    path('privacy/', views_frontend.privacy, name='privacy'),

    # Contact
    path('contact/', views_frontend.contactus, name='contactus'),

    # Utility pages
    path('coming-soon/', views_frontend.comingsoon, name='comingsoon'),
    path('maintenance/', views_frontend.maintenance, name='maintenance'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'core'

urlpatterns = [
    # API URLs
    path('api/v1/', include((api_urlpatterns, 'api'))),

    # Frontend URLs
    path('', include(frontend_urlpatterns)),
]
