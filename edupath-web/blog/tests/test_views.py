"""
Tests for blog frontend views.
"""

import pytest


@pytest.mark.django_db
class TestBlogViews:
    """Tests for blog views."""

    def test_blog_list_view(self, client):
        """Test blog listing page."""
        url = '/blog/'
        response = client.get(url)
        assert response.status_code == 200

    def test_blog_sidebar_view(self, client):
        """Test blog listing with sidebar."""
        url = '/blog/sidebar/'
        response = client.get(url)
        assert response.status_code == 200

    def test_blog_detail_by_slug(self, client, blog):
        """Test blog detail page by slug."""
        url = f'/blog/{blog.slug}/'
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['blog'] == blog

    def test_blog_detail_by_id(self, client, blog):
        """Test blog detail page by ID."""
        url = f'/blog/detail/{blog.pk}/'
        response = client.get(url)
        assert response.status_code == 200

    def test_blog_detail_includes_recent(self, client, blog, instructor, db):
        """Test blog detail includes recent blogs."""
        from blog.models import Blog
        Blog.objects.create(
            title='Recent Blog',
            slug='recent-blog',
            name='Dev',
            content='Content',
            author=instructor,
            img='blog_images/test.jpg'
        )
        url = f'/blog/{blog.slug}/'
        response = client.get(url)
        assert 'recent_blogs' in response.context

    def test_blog_detail_404(self, client):
        """Test 404 for invalid blog slug."""
        url = '/blog/invalid-slug/'
        response = client.get(url)
        assert response.status_code == 404
