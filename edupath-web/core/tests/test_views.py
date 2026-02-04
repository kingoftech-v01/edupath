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
        url = '/aboutus/'
        response = client.get(url)
        assert response.status_code == 200

    def test_features_view(self, client):
        """Test features page."""
        url = '/features/'
        response = client.get(url)
        assert response.status_code == 200

    def test_pricing_view(self, client):
        """Test pricing page."""
        url = '/pricing/'
        response = client.get(url)
        assert response.status_code == 200

    def test_faqs_view(self, client):
        """Test FAQs page."""
        url = '/faqs/'
        response = client.get(url)
        assert response.status_code == 200

    def test_terms_view(self, client):
        """Test terms page."""
        url = '/terms/'
        response = client.get(url)
        assert response.status_code == 200

    def test_privacy_view(self, client):
        """Test privacy page."""
        url = '/privacy/'
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestContactViews:
    """Tests for contact views."""

    def test_contactus_view_get(self, client):
        """Test contact page GET request."""
        url = '/contactus/'
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_contactus_view_post_valid(self, client):
        """Test contact form submission with valid data."""
        url = '/contactus/'
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
        url = '/contactus/'
        response = client.post(url, {
            'name': 'John Doe',
            # Missing required fields
        })
        assert response.status_code == 200  # Re-render form with errors

    def test_contactus_authenticated_user(self, logged_in_client, user):
        """Test contact form links to authenticated user."""
        url = '/contactus/'
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
        url = '/comingsoon/'
        response = client.get(url)
        assert response.status_code == 200

    def test_maintenance_view(self, client):
        """Test maintenance page."""
        url = '/maintenance/'
        response = client.get(url)
        assert response.status_code == 200
