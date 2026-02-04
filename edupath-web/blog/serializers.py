"""
Blog Serializers - API serializers for blog app.
"""

from rest_framework import serializers
from .models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    """Blog serializer for listings."""
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'img', 'name',
            'read_time_minutes', 'publish_date', 'author_name', 'excerpt'
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    """Blog serializer with full details."""
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_title = serializers.CharField(source='author.title', read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'img',
            'name', 'read_time_minutes', 'publish_date',
            'author_name', 'author_title', 'created_at', 'updated_at'
        ]
