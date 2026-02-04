"""
Integration tests for blog workflows.
"""

import pytest

from blog.models import Blog


@pytest.mark.django_db
@pytest.mark.integration
class TestBlogWorkflow:
    """Tests for blog browsing workflow."""

    def test_blog_listing_to_detail(self, client, blog):
        """Test navigating from blog list to detail."""
        # Visit blog listing
        response = client.get('/blog/')
        assert response.status_code == 200

        # Visit blog detail
        response = client.get(f'/blog/{blog.slug}/')
        assert response.status_code == 200
        assert response.context['blog'] == blog

    def test_blog_detail_shows_recent(self, client, blog, instructor, db):
        """Test blog detail shows recent blogs sidebar."""
        # Create another blog
        Blog.objects.create(
            title='Another Blog',
            slug='another-blog',
            name='Dev',
            content='Content',
            author=instructor,
            img='blog_images/test.jpg'
        )

        response = client.get(f'/blog/{blog.slug}/')
        assert len(response.context['recent_blogs']) > 0

    def test_blog_api_list_and_detail(self, api_client, blog):
        """Test blog API list and detail workflow."""
        # List blogs
        response = api_client.get('/blog/api/v1/posts/')
        assert response.status_code == 200
        assert len(response.data['results']) >= 1

        # Get detail
        response = api_client.get(f'/blog/api/v1/posts/{blog.slug}/')
        assert response.status_code == 200
        assert response.data['title'] == blog.title

    def test_blog_api_recent(self, api_client, blog):
        """Test blog API recent endpoint."""
        response = api_client.get('/blog/api/v1/posts/recent/')
        assert response.status_code == 200
        assert isinstance(response.data, list)
