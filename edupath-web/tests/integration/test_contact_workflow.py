"""
Integration tests for contact workflows.
"""

import pytest

from core.models import ContactSubmission


@pytest.mark.django_db
@pytest.mark.integration
class TestContactWorkflow:
    """Tests for contact form submission workflow."""

    def test_anonymous_contact_submission(self, client):
        """Test anonymous user can submit contact form."""
        response = client.post('/core/contact/', {
            'name': 'Anonymous User',
            'email': 'anon@example.com',
            'subject': 'Question',
            'message': 'I have a question about your courses.'
        })
        assert response.status_code == 302

        submission = ContactSubmission.objects.get(email='anon@example.com')
        assert submission.user is None
        assert submission.status == 'new'

    def test_authenticated_contact_submission(self, logged_in_client, user):
        """Test authenticated user contact form links to user."""
        response = logged_in_client.post('/core/contact/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Feedback',
            'message': 'Great platform!'
        })
        assert response.status_code == 302

        submission = ContactSubmission.objects.get(email='test@example.com')
        assert submission.user == user

    def test_contact_api_workflow(self, api_client):
        """Test contact submission via API."""
        response = api_client.post('/core/api/v1/contact/', {
            'name': 'API User',
            'email': 'api@example.com',
            'subject': 'API Test',
            'message': 'Testing API submission'
        })
        assert response.status_code == 201
        assert 'message' in response.data

        submission = ContactSubmission.objects.get(email='api@example.com')
        assert submission.status == 'new'

    def test_contact_validation_workflow(self, client):
        """Test contact form validation prevents invalid submissions."""
        # Try invalid submission
        response = client.post('/core/contact/', {
            'name': 'Test',
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        })
        assert response.status_code == 200  # Form re-rendered with errors
        assert ContactSubmission.objects.count() == 0
