"""
Tests for core forms.
"""

import pytest

from core.forms import ContactForm


@pytest.mark.django_db
class TestContactForm:
    """Tests for ContactForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = ContactForm(data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        assert form.is_valid()

    def test_form_invalid_email(self):
        """Test form with invalid email."""
        form = ContactForm(data={
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_form_missing_required_fields(self):
        """Test form with missing required fields."""
        form = ContactForm(data={})
        assert not form.is_valid()
        assert 'name' in form.errors
        assert 'email' in form.errors
        assert 'subject' in form.errors
        assert 'message' in form.errors

    def test_form_fields(self):
        """Test form has correct fields."""
        form = ContactForm()
        expected_fields = ['name', 'email', 'subject', 'message']
        for field in expected_fields:
            assert field in form.fields

    def test_form_widgets_have_classes(self):
        """Test form widgets have CSS classes."""
        form = ContactForm()
        assert 'class' in form.fields['name'].widget.attrs
        assert 'class' in form.fields['email'].widget.attrs

    def test_form_save(self, db):
        """Test form saves ContactSubmission."""
        form = ContactForm(data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        assert form.is_valid()
        submission = form.save()
        assert submission.pk is not None
        assert submission.name == 'John Doe'
