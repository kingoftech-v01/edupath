"""
Tests for accounts models.
"""

import pytest
from django.contrib.auth.models import User

from accounts.models import UserProfile


@pytest.mark.django_db
class TestUserProfile:
    """Tests for UserProfile model."""

    def test_user_profile_creation(self, user):
        """Test that a UserProfile is created when User is created."""
        assert hasattr(user, 'profile')
        assert isinstance(user.profile, UserProfile)

    def test_user_profile_str(self, user):
        """Test UserProfile string representation."""
        profile = user.profile
        assert str(profile) == f"{user.username}'s profile"

    def test_user_profile_full_name_with_names(self, user):
        """Test full_name property when user has first and last name."""
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        assert user.profile.full_name == 'John Doe'

    def test_user_profile_full_name_without_names(self, db):
        """Test full_name property falls back to username."""
        user = User.objects.create_user(
            username='noname',
            email='noname@example.com',
            password='testpass123'
        )
        assert user.profile.full_name == 'noname'

    def test_user_profile_defaults(self, user):
        """Test default values for UserProfile fields."""
        profile = user.profile
        assert profile.bio == ''
        assert profile.phone == ''
        assert profile.website == ''
        assert profile.email_notifications is True

    def test_profile_save_signal(self, user):
        """Test that saving user also saves profile."""
        profile = user.profile
        profile.bio = 'Updated bio'
        profile.save()
        user.save()

        profile.refresh_from_db()
        assert profile.bio == 'Updated bio'
