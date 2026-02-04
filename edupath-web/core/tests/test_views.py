"""
Tests for core frontend views.
"""

import pytest

from core.models import ContactSubmission


@pytest.mark.django_db
class TestStaticPageViews:
    """Tests for static page views."""

    def test_aboutus_view(self, client):
        """Test about us page."""
        url = '/core/about/'
        response = client.get(url)
        assert response.status_code == 200

    def test_features_view(self, client):
        """Test features page."""
        url = '/core/features/'
        response = client.get(url)
        assert response.status_code == 200

    def test_pricing_view(self, client):
        """Test pricing page."""
        url = '/core/pricing/'
        response = client.get(url)
        assert response.status_code == 200

    def test_faqs_view(self, client):
        """Test FAQs page."""
        url = '/core/faqs/'
        response = client.get(url)
        assert response.status_code == 200

    def test_terms_view(self, client):
        """Test terms page."""
        url = '/core/terms/'
        response = client.get(url)
        assert response.status_code == 200

    def test_privacy_view(self, client):
        """Test privacy page."""
        url = '/core/privacy/'
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestContactViews:
    """Tests for contact views."""

    def test_contactus_view_get(self, client):
        """Test contact page GET request."""
        url = '/core/contact/'
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_contactus_view_post_valid(self, client):
        """Test contact form submission with valid data."""
        url = '/core/contact/'
        response = client.post(url, {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        assert response.status_code == 302  # Redirect on success
        assert ContactSubmission.objects.filter(email='john@example.com').exists()

    def test_contactus_view_post_invalid(self, client):
        """Test contact form submission with invalid data."""
        url = '/core/contact/'
        response = client.post(url, {
            'name': 'John Doe',
            # Missing required fields
        })
        assert response.status_code == 200  # Re-render form with errors

    def test_contactus_authenticated_user(self, logged_in_client, user):
        """Test contact form links to authenticated user."""
        url = '/core/contact/'
        logged_in_client.post(url, {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        submission = ContactSubmission.objects.get(email='john@example.com')
        assert submission.user == user


@pytest.mark.django_db
class TestUtilityPageViews:
    """Tests for utility page views."""

    def test_comingsoon_view(self, client):
        """Test coming soon page."""
        url = '/core/coming-soon/'
        response = client.get(url)
        assert response.status_code == 200

    def test_maintenance_view(self, client):
        """Test maintenance page."""
        url = '/core/maintenance/'
        response = client.get(url)
        assert response.status_code == 200

    def test_not_found_view(self, client):
        """Test notFound view directly (not routed via URL)."""
        from core.views_frontend import notFound
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        rf = RequestFactory()
        request = rf.get('/404/')
        request.user = AnonymousUser()
        response = notFound(request)
        assert response.status_code == 200
