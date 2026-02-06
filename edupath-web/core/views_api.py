"""
Core API Views - REST API endpoints for core functionality.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q

from .models import (
    Feature, BusinessPartner, SiteStatistic, PricingPlan,
    ContactInfo, ContactSubmission, SiteConfiguration
)
from .serializers import (
    FeatureSerializer, BusinessPartnerSerializer,
    SiteStatisticSerializer, PricingPlanSerializer,
    ContactInfoSerializer, ContactSubmissionSerializer,
    SiteConfigurationSerializer
)


# =============================================================================
# STATIC CONTENT VIEWSETS (Read-Only)
# =============================================================================

class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Platform features API.

    Lists all active features for display on homepage.
    """
    queryset = Feature.objects.filter(is_active=True)
    serializer_class = FeatureSerializer
    pagination_class = None


class BusinessPartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Business partner logos API.

    Lists all active partner logos for carousel display.
    """
    queryset = BusinessPartner.objects.filter(is_active=True)
    serializer_class = BusinessPartnerSerializer
    pagination_class = None


class SiteStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Site statistics API.

    Lists statistics for CTA counter animations.
    """
    queryset = SiteStatistic.objects.filter(is_active=True)
    serializer_class = SiteStatisticSerializer
    pagination_class = None


class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Pricing plans API.

    Lists all active pricing plans for pricing page.
    """
    queryset = PricingPlan.objects.filter(is_active=True)
    serializer_class = PricingPlanSerializer
    pagination_class = None


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Contact information API.

    Lists all contact methods for contact page.
    """
    queryset = ContactInfo.objects.filter(is_active=True)
    serializer_class = ContactInfoSerializer
    pagination_class = None


# =============================================================================
# CONTACT SUBMISSION API VIEW
# =============================================================================

class ContactSubmissionAPIView(APIView):
    """
    API endpoint for contact form submissions.

    POST /core/api/v1/contact/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Submit a contact form message.

        Creates a new ContactSubmission. Links to user if authenticated.

        Args:
            request: The HTTP request object with form data.

        Returns:
            Response: Success message or validation errors.
        """
        serializer = ContactSubmissionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Thank you for your message. We will get back to you soon.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# SITE CONFIGURATION API VIEW
# =============================================================================

class SiteConfigurationAPIView(APIView):
    """
    API endpoint for site configuration.

    GET /core/api/v1/site-config/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Get site configuration.

        Returns the singleton site configuration.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Serialized site configuration.
        """
        config = SiteConfiguration.get_solo()
        serializer = SiteConfigurationSerializer(config)
        return Response(serializer.data)


# =============================================================================
# HOMEPAGE DATA API VIEW
# =============================================================================

class HomepageDataAPIView(APIView):
    """
    Combined API endpoint for homepage data.

    GET /core/api/v1/homepage/

    Returns all data needed for the homepage in a single request,
    reducing HTTP roundtrips for mobile/SPA clients.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Get all homepage data in a single request.

        Returns features, partners, categories, courses, instructors,
        reviews, statistics, and blogs. Limits match homepage layout.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Combined homepage data dictionary.
        """
        # Imports inside method to avoid circular imports between core and other apps.
        from courses.models import Category, Course, Instructor
        from courses.serializers import CategoryListSerializer, CourseListSerializer, InstructorListSerializer
        from courses.models import Review
        from courses.serializers import ReviewSerializer
        from blog.models import Blog
        from blog.serializers import BlogListSerializer

        # Limits match homepage layout: 6 featured courses (2 rows of 3),
        # 8 instructors (carousel), 3 blogs (sidebar), 6 reviews (testimonials).
        data = {
            'features': FeatureSerializer(
                Feature.objects.filter(is_active=True), many=True
            ).data,
            'business_partners': BusinessPartnerSerializer(
                BusinessPartner.objects.filter(is_active=True), many=True
            ).data,
            'categories': CategoryListSerializer(
                Category.objects.filter(is_active=True), many=True
            ).data,
            'featured_courses': CourseListSerializer(
                Course.objects.filter(is_active=True, is_featured=True)[:6], many=True
            ).data,
            'instructors': InstructorListSerializer(
                Instructor.objects.filter(is_active=True)[:8], many=True
            ).data,
            'reviews': ReviewSerializer(
                Review.objects.filter(is_active=True)[:6], many=True
            ).data,
            'statistics': SiteStatisticSerializer(
                SiteStatistic.objects.filter(is_active=True), many=True
            ).data,
            'recent_blogs': BlogListSerializer(
                Blog.objects.filter(is_active=True)[:3], many=True
            ).data,
        }
        return Response(data)
