"""
Tests for accounts frontend views.
"""

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProfileViews:
    """Tests for profile views."""

    def test_profile_view_requires_login(self, client):
        """Test that profile view requires login."""
        url = '/accounts/profile/'
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login

    def test_profile_view_authenticated(self, logged_in_client):
        """Test profile view when authenticated."""
        url = '/accounts/profile/'
        response = logged_in_client.get(url)
        assert response.status_code == 200

    def test_profile_edit_requires_login(self, client):
        """Test that profile edit requires login."""
        url = '/accounts/profile/edit/'
        response = client.get(url)
        assert response.status_code == 302

    def test_profile_edit_get(self, logged_in_client):
        """Test profile edit page GET request."""
        url = '/accounts/profile/edit/'
        response = logged_in_client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_profile_edit_post_valid(self, logged_in_client, user):
        """Test profile edit with valid data."""
        url = '/accounts/profile/edit/'
        response = logged_in_client.post(url, {
            'bio': 'Updated bio',
            'phone': '+1234567890',
            'email_notifications': True,
        })
        assert response.status_code == 302  # Redirect on success
        user.profile.refresh_from_db()
        assert user.profile.bio == 'Updated bio'

    def test_profile_edit_updates_user_name(self, logged_in_client, user):
        """Test that profile edit updates User first/last name."""
        url = '/accounts/profile/edit/'
        logged_in_client.post(url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Bio',
            'email_notifications': True,
        })
        user.refresh_from_db()
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'


@pytest.mark.django_db
class TestAuthenticationViews:
    """Tests for authentication views."""

    def test_login_view_get(self, client):
        """Test login page GET request."""
        url = '/accounts/login/'
        response = client.get(url)
        assert response.status_code == 200

    def test_login_view_authenticated_redirect(self, logged_in_client):
        """Test login page redirects if already authenticated."""
        url = '/accounts/login/'
        response = logged_in_client.get(url)
        assert response.status_code == 302

    def test_signup_view_get(self, client):
        """Test signup page GET request."""
        url = '/accounts/signup/'
        response = client.get(url)
        assert response.status_code == 200

    def test_signup_view_authenticated_redirect(self, logged_in_client):
        """Test signup page redirects if already authenticated."""
        url = '/accounts/signup/'
        response = logged_in_client.get(url)
        assert response.status_code == 302

    def test_logout_view(self, logged_in_client):
        """Test logout view."""
        url = '/accounts/logout/'
        response = logged_in_client.get(url)
        assert response.status_code == 302  # Redirect to index

    def test_password_reset_view_get(self, client):
        """Test password reset page GET request."""
        url = '/accounts/password/reset/'
        response = client.get(url)
        assert response.status_code == 200
