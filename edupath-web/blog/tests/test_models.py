"""
Tests for blog models.
"""

import pytest
from django.utils import timezone

from blog.models import Blog


@pytest.mark.django_db
class TestBlog:
    """Tests for Blog model."""

    def test_blog_creation(self, blog):
        """Test Blog instance creation."""
        assert blog.title == 'Test Blog Post'
        assert blog.is_active is True

    def test_blog_str(self, blog):
        """Test Blog string representation."""
        assert str(blog) == 'Test Blog Post'

    def test_blog_slug_auto_generation(self, instructor, db):
        """Test slug is auto-generated from title."""
        blog = Blog.objects.create(
            title='My First Blog Post',
            name='Development',
            content='Content here',
            author=instructor,
            img='blog_images/test.jpg'
        )
        assert blog.slug == 'my-first-blog-post'

    def test_blog_author_relation(self, blog, instructor):
        """Test blog-author relationship."""
        assert blog.author == instructor
        assert blog in instructor.blogs.all()

    def test_blog_ordering(self, instructor, db):
        """Test blogs are ordered by publish_date descending."""
        blog1 = Blog.objects.create(
            title='Blog 1',
            slug='blog-1',
            name='Dev',
            content='Content',
            author=instructor,
            img='blog_images/test1.jpg',
            publish_date=timezone.now().date()
        )
        blog2 = Blog.objects.create(
            title='Blog 2',
            slug='blog-2',
            name='Dev',
            content='Content',
            author=instructor,
            img='blog_images/test2.jpg',
            publish_date=timezone.now().date(),
            order=1
        )
        blogs = list(Blog.objects.all())
        # Both have same publish_date, so ordered by order field
        assert blogs[0].order <= blogs[1].order

    def test_blog_read_time(self, blog):
        """Test read_time_minutes default value."""
        assert blog.read_time_minutes >= 0
