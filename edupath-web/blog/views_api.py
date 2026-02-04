"""
Blog API Views - REST API endpoints.
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Blog listing and detail.

    Endpoints:
    - GET /blog/api/v1/posts/ - List all blogs
    - GET /blog/api/v1/posts/{slug}/ - Blog detail
    - GET /blog/api/v1/posts/recent/ - Recent blogs
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
