"""
Tests for accounts forms.
"""

import pytest

from accounts.forms import UserProfileForm


@pytest.mark.django_db
class TestUserProfileForm:
    """Tests for UserProfileForm."""

    def test_form_valid_data(self, user):
        """Test form with valid data."""
        form = UserProfileForm(data={
            'bio': 'Test bio',
            'phone': '+1234567890',
            'email_notifications': True,
        })
        assert form.is_valid()

    def test_form_includes_first_last_name(self, user):
        """Test form includes first_name and last_name fields."""
        form = UserProfileForm()
        assert 'first_name' in form.fields
        assert 'last_name' in form.fields

    def test_form_optional_fields(self, user):
        """Test form with only required fields."""
        form = UserProfileForm(data={
            'email_notifications': True,
        })
        assert form.is_valid()

    def test_form_url_validation(self, user):
        """Test form URL field validation."""
        form = UserProfileForm(data={
            'website': 'not-a-valid-url',
            'email_notifications': True,
        })
        assert not form.is_valid()
        assert 'website' in form.errors
