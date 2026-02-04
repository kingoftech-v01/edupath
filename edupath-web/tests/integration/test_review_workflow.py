"""
Integration tests for review workflows.
"""

import pytest

from courses.models import Review


@pytest.mark.django_db
@pytest.mark.integration
class TestReviewWorkflow:
    """Tests for course review submission workflow."""

    def test_authenticated_review_submission(self, logged_in_client, course, user):
        """Test authenticated user can submit review via HTMX."""
        response = logged_in_client.post(
            f'/courses/htmx/review/{course.pk}/',
            {
                'desc': 'Excellent course! Learned a lot.',
                'rating': 5
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

        review = Review.objects.get(course=course, user=user)
        assert review.rating == 5
        assert 'Excellent' in review.desc

    def test_review_api_workflow(self, authenticated_client, course, user):
        """Test review submission via API."""
        response = authenticated_client.post('/courses/api/v1/reviews/', {
            'name': user.username,
            'desc': 'API Review',
            'rating': 4,
            'course': course.pk
        })
        assert response.status_code == 201

        review = Review.objects.get(course=course, desc='API Review')
        assert review.rating == 4

    def test_review_appears_on_course_page(self, client, course, review):
        """Test review appears on course detail page."""
        response = client.get(f'/courses/{course.slug}/')
        assert response.status_code == 200
        assert review in response.context['course_reviews']

    def test_unauthenticated_review_blocked(self, client, course):
        """Test unauthenticated users cannot submit reviews."""
        response = client.post(
            f'/courses/htmx/review/{course.pk}/',
            {
                'desc': 'Should not work',
                'rating': 5
            }
        )
        assert response.status_code == 302  # Redirect to login
        assert Review.objects.filter(course=course).count() == 0
