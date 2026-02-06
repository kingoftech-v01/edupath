"""Courses API views."""

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


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only category endpoints with nested courses action."""
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
        """List courses in this category."""
        category = self.get_object()
        courses = category.courses.filter(is_active=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only instructor endpoints with nested courses action."""
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
        """List courses by this instructor."""
        instructor = self.get_object()
        courses = instructor.courses.filter(is_active=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """Full CRUD for courses. Write ops require admin."""
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'instructor', 'is_free', 'is_featured']
    search_fields = ['title', 'desc', 'name']
    ordering_fields = ['price', 'students', 'created_at', 'order']
    ordering = ['order', '-created_at']

    def get_queryset(self):
        # select_related prevents N+1 when serializing nested category/instructor
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
        """Homepage featured section (limit 6)."""
        courses = self.get_queryset().filter(is_featured=True)[:6]
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def free(self, request):
        courses = self.get_queryset().filter(is_free=True)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Same-category courses for sidebar (limit 4)."""
        course = self.get_object()
        related = Course.objects.filter(
            category=course.category,
            is_active=True
        ).exclude(pk=course.pk)[:4]
        serializer = CourseListSerializer(related, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Reviews with auth-gated creation for spam prevention."""
    queryset = Review.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        # Login required for create (spam prevention), admin for modify/delete (moderation)
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
