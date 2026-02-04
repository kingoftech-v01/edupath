"""
Tests for courses frontend views.
"""

import pytest
from django.urls import reverse

from courses.models import Course, Review


@pytest.mark.django_db
class TestCourseListViews:
    """Tests for course listing views."""

    def test_course_list_view(self, client, course):
        """Test course list page."""
        url = '/courses/'
        response = client.get(url)
        assert response.status_code == 200
        assert 'courses' in response.context

    def test_course_list_filter_by_category(self, client, course, category):
        """Test course list filtered by category."""
        url = f'/courses/?category={category.slug}'
        response = client.get(url)
        assert response.status_code == 200

    def test_course_list_search(self, client, course):
        """Test course list search functionality."""
        url = '/courses/?search=Test'
        response = client.get(url)
        assert response.status_code == 200

    def test_course_list_filter_free(self, client, course):
        """Test course list filtered to free courses."""
        url = '/courses/?price=free'
        response = client.get(url)
        assert response.status_code == 200

    def test_course_list_filter_paid(self, client, course):
        """Test course list filtered to paid courses."""
        url = '/courses/?price=paid'
        response = client.get(url)
        assert response.status_code == 200

    def test_course_list_pagination(self, client, category, instructor, db):
        """Test course list pagination."""
        # Create multiple courses
        for i in range(15):
            Course.objects.create(
                title=f'Course {i}',
                slug=f'course-{i}',
                desc='Test',
                category=category,
                instructor=instructor
            )
        url = '/courses/?page=2'
        response = client.get(url)
        assert response.status_code == 200

    def test_grid_view(self, client):
        """Test grid listing view."""
        url = '/courses/grid/'
        response = client.get(url)
        assert response.status_code == 200

    def test_grid_sidebar_view(self, client):
        """Test grid with sidebar view."""
        url = '/courses/grid-sidebar/'
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view(self, client):
        """Test list view page."""
        url = '/courses/list/'
        response = client.get(url)
        assert response.status_code == 200

    def test_list_sidebar_view(self, client):
        """Test list with sidebar view."""
        url = '/courses/list-sidebar/'
        response = client.get(url)
        assert response.status_code == 200

    def test_youtube_listing_view(self, client):
        """Test YouTube listing view."""
        url = '/courses/youtube/'
        response = client.get(url)
        assert response.status_code == 200

    def test_video_listing_view(self, client):
        """Test video listing view."""
        url = '/courses/video/'
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestCourseDetailViews:
    """Tests for course detail views."""

    def test_course_detail_by_slug(self, client, course):
        """Test course detail page by slug."""
        url = f'/courses/{course.slug}/'
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['course'] == course

    def test_course_detail_by_id(self, client, course):
        """Test course detail page by ID."""
        url = f'/courses/detail/{course.pk}/'
        response = client.get(url)
        assert response.status_code == 200

    def test_course_detail_includes_related(self, client, course, category, instructor, db):
        """Test course detail includes related courses."""
        # Create related course in same category
        Course.objects.create(
            title='Related Course',
            slug='related-course',
            desc='Related',
            category=category,
            instructor=instructor
        )
        url = f'/courses/{course.slug}/'
        response = client.get(url)
        assert 'courses3' in response.context

    def test_course_detail_includes_reviews(self, client, course, review):
        """Test course detail includes reviews."""
        url = f'/courses/{course.slug}/'
        response = client.get(url)
        assert 'course_reviews' in response.context

    def test_course_detail_404_invalid_slug(self, client):
        """Test 404 for invalid course slug."""
        url = '/courses/invalid-slug/'
        response = client.get(url)
        assert response.status_code == 404

    def test_course_detail_two(self, client, course):
        """Test alternative course detail page."""
        url = f'/courses/detail-two/{course.pk}/'
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestInstructorViews:
    """Tests for instructor views."""

    def test_instructor_list_view(self, client):
        """Test instructor listing page."""
        url = '/courses/instructors/'
        response = client.get(url)
        assert response.status_code == 200

    def test_instructor_detail_view(self, client, instructor, course):
        """Test instructor detail page."""
        url = f'/courses/instructors/{instructor.slug}/'
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['instructor'] == instructor

    def test_instructor_detail_404(self, client):
        """Test 404 for invalid instructor slug."""
        url = '/courses/instructors/invalid-slug/'
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestCategoryViews:
    """Tests for category views."""

    def test_category_list_view(self, client, category):
        """Test category listing page."""
        url = '/courses/categories/'
        response = client.get(url)
        assert response.status_code == 200
        assert 'categories' in response.context

    def test_category_detail_view(self, client, category, course):
        """Test category detail page."""
        url = f'/courses/categories/{category.slug}/'
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['category'] == category


@pytest.mark.django_db
class TestHtmxViews:
    """Tests for HTMX views."""

    def test_htmx_course_list(self, client, course):
        """Test HTMX course list endpoint."""
        url = '/courses/htmx/course-list/'
        response = client.get(url)
        assert response.status_code == 200

    def test_htmx_course_list_filter(self, client, course, category):
        """Test HTMX course list with filters."""
        url = f'/courses/htmx/course-list/?category={category.slug}'
        response = client.get(url)
        assert response.status_code == 200

    def test_htmx_submit_review_requires_auth(self, client, course):
        """Test HTMX review submission requires auth."""
        url = f'/courses/htmx/review/{course.pk}/'
        response = client.post(url, {
            'desc': 'Great course!',
            'rating': 5
        })
        assert response.status_code == 302  # Redirect to login

    def test_htmx_submit_review_authenticated(self, logged_in_client, course, user):
        """Test HTMX review submission when authenticated."""
        url = f'/courses/htmx/review/{course.pk}/'
        response = logged_in_client.post(url, {
            'desc': 'Great course!',
            'rating': 5
        })
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_htmx_course_list_search(self, client, course):
        """Test HTMX course list with search filter."""
        url = '/courses/htmx/course-list/?search=Test'
        response = client.get(url)
        assert response.status_code == 200

    def test_htmx_submit_review_invalid_form(self, logged_in_client, course):
        """Test HTMX review submission with invalid form data."""
        url = f'/courses/htmx/review/{course.pk}/'
        response = logged_in_client.post(url, {
            'desc': '',
            'rating': ''
        })
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
