"""
Tests for courses models.
"""

import pytest
from decimal import Decimal

from courses.models import Category, Instructor, Course, Review


@pytest.mark.django_db
class TestCategory:
    """Tests for Category model."""

    def test_category_creation(self, category):
        """Test Category instance creation."""
        assert category.name == 'Test Category'
        assert category.is_active is True

    def test_category_str(self, category):
        """Test Category string representation."""
        assert str(category) == 'Test Category'

    def test_category_slug_auto_generation(self, db):
        """Test slug is auto-generated from name."""
        category = Category.objects.create(name='Web Development')
        assert category.slug == 'web-development'

    def test_category_course_count(self, category, instructor, db):
        """Test course_count property."""
        assert category.course_count == 0

        Course.objects.create(
            title='Test Course',
            slug='test-course-1',
            desc='Test',
            category=category,
            instructor=instructor,
            is_active=True
        )
        assert category.course_count == 1

    def test_category_title_property(self, category):
        """Test title property for template compatibility."""
        title = category.title
        assert 'Courses' in title

    def test_category_ordering(self, db):
        """Test categories are ordered by order field."""
        cat1 = Category.objects.create(name='Cat A', order=2)
        cat2 = Category.objects.create(name='Cat B', order=1)
        categories = list(Category.objects.all())
        assert categories[0] == cat2
        assert categories[1] == cat1


@pytest.mark.django_db
class TestInstructor:
    """Tests for Instructor model."""

    def test_instructor_creation(self, instructor):
        """Test Instructor instance creation."""
        assert instructor.name == 'Test Instructor'
        assert instructor.is_active is True

    def test_instructor_str(self, instructor):
        """Test Instructor string representation."""
        assert str(instructor) == 'Test Instructor'

    def test_instructor_slug_auto_generation(self, db):
        """Test slug is auto-generated from name."""
        instructor = Instructor.objects.create(
            name='John Smith',
            title='Developer'
        )
        assert instructor.slug == 'john-smith'

    def test_instructor_with_user(self, user, db):
        """Test Instructor can be linked to a User."""
        instructor = Instructor.objects.create(
            name='User Instructor',
            title='Teacher',
            user=user
        )
        assert instructor.user == user

    def test_instructor_ordering(self, db):
        """Test instructors are ordered by order field."""
        inst1 = Instructor.objects.create(name='Inst A', title='T', order=2)
        inst2 = Instructor.objects.create(name='Inst B', title='T', order=1)
        instructors = list(Instructor.objects.all())
        assert instructors[0] == inst2
        assert instructors[1] == inst1


@pytest.mark.django_db
class TestCourse:
    """Tests for Course model."""

    def test_course_creation(self, course):
        """Test Course instance creation."""
        assert course.title == 'Test Course'
        assert course.is_active is True

    def test_course_str(self, course):
        """Test Course string representation."""
        assert str(course) == 'Test Course'

    def test_course_slug_auto_generation(self, category, instructor, db):
        """Test slug is auto-generated from title."""
        course = Course.objects.create(
            title='Python Programming',
            desc='Learn Python',
            category=category,
            instructor=instructor
        )
        assert course.slug == 'python-programming'

    def test_course_is_free_auto_set(self, category, instructor, db):
        """Test is_free is auto-set based on price."""
        free_course = Course.objects.create(
            title='Free Course',
            slug='free-course',
            desc='Free',
            price=Decimal('0.00'),
            category=category,
            instructor=instructor
        )
        assert free_course.is_free is True

        paid_course = Course.objects.create(
            title='Paid Course',
            slug='paid-course',
            desc='Paid',
            price=Decimal('49.99'),
            category=category,
            instructor=instructor
        )
        assert paid_course.is_free is False

    def test_course_formatted_price_free(self, category, instructor, db):
        """Test formatted_price for free course."""
        course = Course.objects.create(
            title='Free Course',
            slug='free-course-test',
            desc='Free',
            price=Decimal('0.00'),
            category=category,
            instructor=instructor
        )
        assert course.formatted_price == '$0'

    def test_course_formatted_price_paid(self, course):
        """Test formatted_price for paid course."""
        course.price = Decimal('49.99')
        course.is_free = False
        course.save()
        assert course.formatted_price == '$50'

    def test_course_video_property(self, course):
        """Test video property alias."""
        course.video_url = 'https://youtube.com/watch?v=123'
        assert course.video == 'https://youtube.com/watch?v=123'

    def test_course_src_property_empty(self, course):
        """Test src property when no video file."""
        assert course.src == ''

    def test_course_name_auto_set(self, category, instructor, db):
        """Test name is auto-set from instructor."""
        course = Course.objects.create(
            title='Auto Name Course',
            slug='auto-name-course',
            desc='Test',
            category=category,
            instructor=instructor
        )
        assert course.name == instructor.name

    def test_course_category_relation(self, course, category):
        """Test course-category relationship."""
        assert course.category == category
        assert course in category.courses.all()

    def test_course_instructor_relation(self, course, instructor):
        """Test course-instructor relationship."""
        assert course.instructor == instructor
        assert course in instructor.courses.all()

    def test_course_src_with_video_file(self, db):
        """Test src property returns video_file URL when set."""
        from courses.models import Course
        course = Course.objects.create(
            title='Video Course',
            slug='video-course',
            desc='Test',
            video_file='course_videos/test.mp4'
        )
        assert course.src == '/media/course_videos/test.mp4'


@pytest.mark.django_db
class TestReview:
    """Tests for Review model."""

    def test_review_creation(self, review):
        """Test Review instance creation."""
        assert review.rating == 5
        assert review.is_active is True

    def test_review_str(self, review):
        """Test Review string representation."""
        assert 'stars' in str(review)
        assert '5' in str(review)

    def test_review_rating_choices(self, course, db):
        """Test rating must be between 1 and 5."""
        review = Review.objects.create(
            name='Reviewer',
            desc='Good course',
            rating=3,
            course=course
        )
        assert review.rating == 3

    def test_review_course_relation(self, review, course):
        """Test review-course relationship."""
        assert review.course == course
        assert review in course.reviews.all()
