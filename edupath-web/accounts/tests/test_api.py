"""
Tests for accounts API views.
"""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserProfileViewSet:
    """Tests for UserProfileViewSet."""

    def test_profile_list_requires_admin(self, authenticated_client):
        """Test that listing profiles requires admin permission."""
        url = '/accounts/api/v1/profiles/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_profile_list_admin_success(self, admin_client):
        """Test that admin can list profiles."""
        url = '/accounts/api/v1/profiles/'
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_profile_me_get(self, authenticated_client, user):
        """Test getting current user's profile."""
        url = '/accounts/api/v1/profiles/me/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'bio' in response.data

    def test_profile_me_patch(self, authenticated_client, user):
        """Test updating current user's profile."""
        url = '/accounts/api/v1/profiles/me/'
        response = authenticated_client.patch(url, {'bio': 'Updated bio'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'Updated bio'

    def test_profile_me_requires_auth(self, api_client):
        """Test that /me/ endpoint requires authentication."""
        url = '/accounts/api/v1/profiles/me/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_profile_retrieve(self, authenticated_client, user):
        """Test retrieving own profile by id."""
        url = f'/accounts/api/v1/profiles/{user.profile.pk}/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_profile_me_patch_invalid(self, authenticated_client, user):
        """Test updating profile with invalid data returns 400."""
        url = '/accounts/api/v1/profiles/me/'
        response = authenticated_client.patch(url, {'website': 'not-a-url'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCurrentUserAPIView:
    """Tests for CurrentUserAPIView."""

    def test_current_user_authenticated(self, authenticated_client, user):
        """Test getting current user info when authenticated."""
        url = '/accounts/api/v1/me/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_current_user_unauthenticated(self, api_client):
        """Test that endpoint requires authentication."""
        url = '/accounts/api/v1/me/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
