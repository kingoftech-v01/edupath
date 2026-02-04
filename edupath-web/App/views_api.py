"""
EduPath API Views - REST API endpoints using Django REST Framework.

Provides:
- ViewSets for CRUD operations
- Custom API views for specific endpoints
- Filtering, search, and pagination

API URL namespace: api:v1:App:resource-name
"""

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import (
    Category, Instructor, Course, Blog, Review, Feature,
    BusinessPartner, SiteStatistic, PricingPlan, ContactInfo,
    ContactSubmission, SiteConfiguration
)
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    InstructorListSerializer, InstructorDetailSerializer,
    CourseListSerializer, CourseDetailSerializer, CourseCreateUpdateSerializer,
    BlogListSerializer, BlogDetailSerializer,
    ReviewSerializer, ReviewCreateSerializer,
    FeatureSerializer, BusinessPartnerSerializer,
    SiteStatisticSerializer, PricingPlanSerializer,
    ContactInfoSerializer, ContactSubmissionSerializer,
    SiteConfigurationSerializer
)


# =============================================================================
# CATEGORY VIEWSET
# =============================================================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category listing and detail.

    Endpoints:
    - GET /api/v1/categories/ - List all categories
    - GET /api/v1/categories/{slug}/ - Category detail
    """
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order']
    ordering = ['order']

    def get_queryset(self):
        return Category.objects.filter(is_active=True).annotate(
            course_count=Count('courses', filter=Q(courses__is_active=True))
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, slug=None):
        """Get courses in this category."""
        category = self.get_object()
        courses = category.courses.filter(is_active=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


# =============================================================================
# INSTRUCTOR VIEWSET
# =============================================================================

class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Instructor listing and detail.

    Endpoints:
    - GET /api/v1/instructors/ - List all instructors
    - GET /api/v1/instructors/{slug}/ - Instructor detail with courses
    """
    queryset = Instructor.objects.filter(is_active=True)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'title', 'bio']
    ordering_fields = ['name', 'order']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InstructorDetailSerializer
        return InstructorListSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, slug=None):
        """Get courses by this instructor."""
        instructor = self.get_object()
        courses = instructor.courses.filter(is_active=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def blogs(self, request, slug=None):
        """Get blogs by this instructor."""
        instructor = self.get_object()
        blogs = instructor.blogs.filter(is_active=True)
        serializer = BlogListSerializer(blogs, many=True)
        return Response(serializer.data)


# =============================================================================
# COURSE VIEWSET
# =============================================================================

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course CRUD operations.

    Endpoints:
    - GET /api/v1/courses/ - List all courses (filterable)
    - GET /api/v1/courses/{slug}/ - Course detail
    - POST /api/v1/courses/ - Create course (staff only)
    - PUT/PATCH /api/v1/courses/{slug}/ - Update course (staff only)
    - DELETE /api/v1/courses/{slug}/ - Delete course (staff only)

    Custom actions:
    - GET /api/v1/courses/featured/ - Featured courses
    - GET /api/v1/courses/free/ - Free courses
    - GET /api/v1/courses/{slug}/related/ - Related courses

    Filters:
    - ?category=web-development
    - ?instructor=1
    - ?is_free=true
    - ?is_featured=true
    - ?search=python
    """
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'instructor', 'is_free', 'is_featured']
    search_fields = ['title', 'desc', 'name']
    ordering_fields = ['price', 'students', 'created_at', 'order']
    ordering = ['order', '-created_at']

    def get_queryset(self):
        return Course.objects.filter(is_active=True).select_related('category', 'instructor')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured courses."""
        courses = self.get_queryset().filter(is_featured=True)[:6]
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def free(self, request):
        """Get free courses."""
        courses = self.get_queryset().filter(is_free=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Get related courses (same category)."""
        course = self.get_object()
        related = Course.objects.filter(
            category=course.category,
            is_active=True
        ).exclude(pk=course.pk)[:4]
        serializer = CourseListSerializer(related, many=True)
        return Response(serializer.data)


# =============================================================================
# BLOG VIEWSET
# =============================================================================

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Blog listing and detail.

    Endpoints:
    - GET /api/v1/blogs/ - List all blogs
    - GET /api/v1/blogs/{slug}/ - Blog detail
    """
    queryset = Blog.objects.filter(is_active=True).select_related('author')
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['publish_date', 'created_at']
    ordering = ['-publish_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogDetailSerializer
        return BlogListSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts."""
        blogs = self.get_queryset()[:5]
        serializer = BlogListSerializer(blogs, many=True)
        return Response(serializer.data)


# =============================================================================
# REVIEW VIEWSET
# =============================================================================

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reviews.

    Endpoints:
    - GET /api/v1/reviews/ - List reviews
    - POST /api/v1/reviews/ - Create review (authenticated)
    """
    queryset = Review.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# =============================================================================
# STATIC CONTENT VIEWSETS (Read-Only)
# =============================================================================

class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """Platform features."""
    queryset = Feature.objects.filter(is_active=True)
    serializer_class = FeatureSerializer
    pagination_class = None


class BusinessPartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """Business partner logos."""
    queryset = BusinessPartner.objects.filter(is_active=True)
    serializer_class = BusinessPartnerSerializer
    pagination_class = None


class SiteStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """Site statistics for CTA sections."""
    queryset = SiteStatistic.objects.filter(is_active=True)
    serializer_class = SiteStatisticSerializer
    pagination_class = None


class PricingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Pricing plans."""
    queryset = PricingPlan.objects.filter(is_active=True)
    serializer_class = PricingPlanSerializer
    pagination_class = None


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """Contact information."""
    queryset = ContactInfo.objects.filter(is_active=True)
    serializer_class = ContactInfoSerializer
    pagination_class = None


# =============================================================================
# CONTACT SUBMISSION API VIEW
# =============================================================================

class ContactSubmissionAPIView(APIView):
    """
    API endpoint for contact form submissions.

    POST /api/v1/contact/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
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

    GET /api/v1/site-config/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        config = SiteConfiguration.get_solo()
        serializer = SiteConfigurationSerializer(config)
        return Response(serializer.data)


# =============================================================================
# HOMEPAGE DATA API VIEW
# =============================================================================

class HomepageDataAPIView(APIView):
    """
    Combined API endpoint for homepage data.

    GET /api/v1/homepage/

    Returns all data needed for the homepage in a single request.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = {
            'features': FeatureSerializer(
                Feature.objects.filter(is_active=True), many=True
            ).data,
            'business_partners': BusinessPartnerSerializer(
                BusinessPartner.objects.filter(is_active=True), many=True
            ).data,
            'categories': CategoryListSerializer(
                Category.objects.filter(is_active=True).annotate(
                    course_count=Count('courses', filter=Q(courses__is_active=True))
                ), many=True
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
