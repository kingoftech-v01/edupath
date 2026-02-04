"""
Tests for blog API views.
"""

import pytest
from rest_framework import status

from blog.models import Blog


@pytest.mark.django_db
class TestBlogViewSet:
    """Tests for BlogViewSet."""

    def test_blog_list(self, api_client, blog):
        """Test listing blog posts."""
        url = '/blog/api/v1/posts/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_blog_detail(self, api_client, blog):
        """Test retrieving blog post by slug."""
        url = f'/blog/api/v1/posts/{blog.slug}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == blog.title

    def test_blog_recent_action(self, api_client, blog):
        """Test getting recent blog posts."""
        url = '/blog/api/v1/posts/recent/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_blog_search(self, api_client, blog):
        """Test blog search filter."""
        url = '/blog/api/v1/posts/?search=Test'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_blog_filter_by_category(self, api_client, blog):
        """Test filtering blogs by category name."""
        url = f'/blog/api/v1/posts/?name={blog.name}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_blog_ordering(self, api_client, blog):
        """Test blog ordering."""
        url = '/blog/api/v1/posts/?ordering=-publish_date'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_blog_inactive_not_listed(self, api_client, instructor, db):
        """Test that inactive blogs are not listed."""
        Blog.objects.create(
            title='Inactive Blog',
            slug='inactive-blog',
            name='Dev',
            content='Content',
            author=instructor,
            img='blog_images/test.jpg',
            is_active=False
        )
        url = '/blog/api/v1/posts/'
        response = api_client.get(url)
        slugs = [b['slug'] for b in response.data['results']]
        assert 'inactive-blog' not in slugs

    def test_blog_detail_includes_author(self, api_client, blog):
        """Test that blog detail includes author info."""
        url = f'/blog/api/v1/posts/{blog.slug}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'author' in response.data
