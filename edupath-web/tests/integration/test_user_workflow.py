"""
Integration tests for user workflows.
"""

import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
@pytest.mark.integration
class TestUserRegistrationWorkflow:
    """Tests for user registration and profile workflow."""

    def test_profile_created_on_user_creation(self, db):
        """Test that UserProfile is automatically created when User is created."""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='testpass123'
        )
        assert hasattr(user, 'profile')
        assert user.profile is not None

    def test_user_can_update_profile(self, logged_in_client, user):
        """Test complete workflow of user updating their profile."""
        # Get profile edit page
        response = logged_in_client.get('/accounts/profile/edit/')
        assert response.status_code == 200

        # Submit profile update
        response = logged_in_client.post('/accounts/profile/edit/', {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio',
            'email_notifications': True,
        })
        assert response.status_code == 302

        # Verify changes
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
        assert user.profile.bio == 'Updated bio'

    def test_user_api_profile_workflow(self, authenticated_client, user):
        """Test API workflow for getting and updating profile."""
        # Get current profile
        response = authenticated_client.get('/accounts/api/v1/profiles/me/')
        assert response.status_code == 200
        assert 'bio' in response.data

        # Update profile
        response = authenticated_client.patch('/accounts/api/v1/profiles/me/', {
            'bio': 'API updated bio'
        })
        assert response.status_code == 200
        assert response.data['bio'] == 'API updated bio'

    def test_logout_clears_session(self, logged_in_client):
        """Test logout properly clears session."""
        # Access protected page
        response = logged_in_client.get('/accounts/profile/')
        assert response.status_code == 200

        # Logout
        response = logged_in_client.get('/accounts/logout/')
        assert response.status_code == 302

        # Verify can't access protected page
        response = logged_in_client.get('/accounts/profile/')
        assert response.status_code == 302  # Redirect to login
