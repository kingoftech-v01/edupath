"""
Courses API Views - REST API endpoints.
"""

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Category, Instructor, Course, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    InstructorListSerializer, InstructorDetailSerializer,
    CourseListSerializer, CourseDetailSerializer, CourseCreateUpdateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)


# =============================================================================
# CATEGORY VIEWSET
# =============================================================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category listing and detail.

    Endpoints:
    - GET /courses/api/v1/categories/ - List all categories
    - GET /courses/api/v1/categories/{slug}/ - Category detail
    - GET /courses/api/v1/categories/{slug}/courses/ - Courses in category
    """
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order']
    ordering = ['order']

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

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
    - GET /courses/api/v1/instructors/ - List all instructors
    - GET /courses/api/v1/instructors/{slug}/ - Instructor detail
    - GET /courses/api/v1/instructors/{slug}/courses/ - Instructor's courses
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


# =============================================================================
# COURSE VIEWSET
# =============================================================================

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course CRUD operations.

    Endpoints:
    - GET /courses/api/v1/courses/ - List all courses
    - GET /courses/api/v1/courses/{slug}/ - Course detail
    - POST /courses/api/v1/courses/ - Create course (staff)
    - PUT/PATCH /courses/api/v1/courses/{slug}/ - Update course (staff)
    - DELETE /courses/api/v1/courses/{slug}/ - Delete course (staff)

    Custom actions:
    - GET /courses/api/v1/courses/featured/ - Featured courses
    - GET /courses/api/v1/courses/free/ - Free courses
    - GET /courses/api/v1/courses/{slug}/related/ - Related courses
    """
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'instructor', 'is_free', 'is_featured']
    search_fields = ['title', 'desc', 'name']
    ordering_fields = ['price', 'students', 'created_at', 'order']
    ordering = ['order', '-created_at']

    def get_queryset(self):
        # select_related prevents N+1 queries when serializing nested category/instructor.
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
        """Get related courses (same category, excluding current)."""
        course = self.get_object()
        # "Related" = same category. Limit to 4 for sidebar display on course detail page.
        related = Course.objects.filter(
            category=course.category,
            is_active=True
        ).exclude(pk=course.pk)[:4]
        serializer = CourseListSerializer(related, many=True)
        return Response(serializer.data)


# =============================================================================
# REVIEW VIEWSET
# =============================================================================

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reviews.

    Endpoints:
    - GET /courses/api/v1/reviews/ - List reviews
    - POST /courses/api/v1/reviews/ - Create review (authenticated)
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
        # Reviews are public read, require login to create (prevents spam),
        # and only admins can modify/delete (moderation control).
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
