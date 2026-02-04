"""
Tests for courses API views.
"""

import pytest
from rest_framework import status

from courses.models import Category, Instructor, Course, Review


@pytest.mark.django_db
class TestCategoryViewSet:
    """Tests for CategoryViewSet."""

    def test_category_list(self, api_client, category):
        """Test listing categories."""
        url = '/courses/api/v1/categories/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_category_detail(self, api_client, category):
        """Test retrieving category by slug."""
        url = f'/courses/api/v1/categories/{category.slug}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == category.name

    def test_category_courses_action(self, api_client, category, course):
        """Test getting courses in a category."""
        url = f'/courses/api/v1/categories/{category.slug}/courses/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_category_search(self, api_client, category):
        """Test category search filter."""
        url = '/courses/api/v1/categories/?search=Test'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_category_ordering(self, api_client, category):
        """Test category ordering."""
        url = '/courses/api/v1/categories/?ordering=name'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_category_inactive_not_listed(self, api_client, db):
        """Test that inactive categories are not listed."""
        Category.objects.create(name='Inactive Cat', is_active=False)
        url = '/courses/api/v1/categories/'
        response = api_client.get(url)
        slugs = [c['slug'] for c in response.data['results']]
        assert 'inactive-cat' not in slugs


@pytest.mark.django_db
class TestInstructorViewSet:
    """Tests for InstructorViewSet."""

    def test_instructor_list(self, api_client, instructor):
        """Test listing instructors."""
        url = '/courses/api/v1/instructors/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_instructor_detail(self, api_client, instructor):
        """Test retrieving instructor by slug."""
        url = f'/courses/api/v1/instructors/{instructor.slug}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == instructor.name

    def test_instructor_courses_action(self, api_client, instructor, course):
        """Test getting courses by instructor."""
        url = f'/courses/api/v1/instructors/{instructor.slug}/courses/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_instructor_search(self, api_client, instructor):
        """Test instructor search filter."""
        url = '/courses/api/v1/instructors/?search=Test'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseViewSet:
    """Tests for CourseViewSet."""

    def test_course_list(self, api_client, course):
        """Test listing courses."""
        url = '/courses/api/v1/courses/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_course_detail(self, api_client, course):
        """Test retrieving course by slug."""
        url = f'/courses/api/v1/courses/{course.slug}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == course.title

    def test_course_featured_action(self, api_client, course):
        """Test getting featured courses."""
        url = '/courses/api/v1/courses/featured/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_course_free_action(self, api_client, category, instructor, db):
        """Test getting free courses."""
        Course.objects.create(
            title='Free Course',
            slug='free-course-api-test',
            desc='Free',
            price='0.00',
            category=category,
            instructor=instructor,
            is_active=True
        )
        url = '/courses/api/v1/courses/free/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_course_related_action(self, api_client, course):
        """Test getting related courses."""
        url = f'/courses/api/v1/courses/{course.slug}/related/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_course_create_requires_admin(self, authenticated_client, category, instructor):
        """Test that creating course requires admin."""
        url = '/courses/api/v1/courses/'
        data = {
            'title': 'New Course',
            'desc': 'Description',
            'category': category.pk,
            'instructor': instructor.pk
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_course_create_admin_success(self, admin_client, category, instructor):
        """Test that admin can create course."""
        url = '/courses/api/v1/courses/'
        data = {
            'title': 'Admin Course',
            'desc': 'Description',
            'category': category.pk,
            'instructor': instructor.pk,
            'price': '29.99'
        }
        response = admin_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_course_update_requires_admin(self, authenticated_client, course):
        """Test that updating course requires admin."""
        url = f'/courses/api/v1/courses/{course.slug}/'
        response = authenticated_client.patch(url, {'title': 'Updated'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_course_delete_requires_admin(self, authenticated_client, course):
        """Test that deleting course requires admin."""
        url = f'/courses/api/v1/courses/{course.slug}/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_course_search(self, api_client, course):
        """Test course search filter."""
        url = '/courses/api/v1/courses/?search=Test'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_course_filter_by_category(self, api_client, course, category):
        """Test filtering courses by category."""
        url = f'/courses/api/v1/courses/?category__slug={category.slug}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_course_filter_free(self, api_client, course):
        """Test filtering free courses."""
        url = '/courses/api/v1/courses/?is_free=true'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestReviewViewSet:
    """Tests for ReviewViewSet."""

    def test_review_list(self, api_client, review):
        """Test listing reviews."""
        url = '/courses/api/v1/reviews/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_review_create_requires_auth(self, api_client, course):
        """Test that creating review requires authentication."""
        url = '/courses/api/v1/reviews/'
        data = {
            'name': 'Reviewer',
            'desc': 'Great course',
            'rating': 5,
            'course': course.pk
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_review_create_authenticated(self, authenticated_client, course):
        """Test creating review when authenticated."""
        url = '/courses/api/v1/reviews/'
        data = {
            'name': 'Reviewer',
            'desc': 'Great course',
            'rating': 5,
            'course': course.pk
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_review_filter_by_course(self, api_client, review, course):
        """Test filtering reviews by course."""
        url = f'/courses/api/v1/reviews/?course={course.pk}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_review_filter_by_rating(self, api_client, review):
        """Test filtering reviews by rating."""
        url = '/courses/api/v1/reviews/?rating=5'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_review_update_requires_admin(self, authenticated_client, review):
        """Test that updating review requires admin."""
        url = f'/courses/api/v1/reviews/{review.pk}/'
        response = authenticated_client.patch(url, {'rating': 4})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_review_delete_requires_admin(self, authenticated_client, review):
        """Test that deleting review requires admin."""
        url = f'/courses/api/v1/reviews/{review.pk}/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
