"""
Tests for core context processors.

Targets uncovered lines in core/context_processors.py:
- Lines 56-57: site_config except block (SiteConfiguration.get_solo() raises)
- Lines 73-77: global_courses course_id try/except block
- Lines 114-118: global_blogs blog_id try/except block
"""

import pytest
from unittest.mock import patch

from django.test import RequestFactory

from core.context_processors import (
    global_business_data,
    global_features,
    global_ctas,
    global_pages,
    global_contacts,
    site_config,
    global_courses,
    global_instructors,
    global_categories,
    global_reviews,
    global_blogs,
    global_courses1,
    global_courses2,
    global_courses3,
    user_info,
)


@pytest.fixture
def rf():
    """Return a Django RequestFactory instance."""
    return RequestFactory()


@pytest.fixture
def request_obj(rf):
    """Return a basic GET request."""
    return rf.get('/')


# =============================================================================
# SIMPLE QUERYSET CONTEXT PROCESSORS
# =============================================================================


@pytest.mark.django_db
class TestGlobalBusinessData:
    """Tests for global_business_data context processor."""

    def test_returns_business_key(self, request_obj):
        """Test that result contains 'business' key."""
        result = global_business_data(request_obj)
        assert 'business' in result

    def test_includes_active_partner(self, request_obj, business_partner):
        """Test that active business partners appear in queryset."""
        result = global_business_data(request_obj)
        assert business_partner in result['business']


@pytest.mark.django_db
class TestGlobalFeatures:
    """Tests for global_features context processor."""

    def test_returns_features_key(self, request_obj):
        """Test that result contains 'features' key."""
        result = global_features(request_obj)
        assert 'features' in result

    def test_includes_active_feature(self, request_obj, feature):
        """Test that active features appear in queryset."""
        result = global_features(request_obj)
        assert feature in result['features']


@pytest.mark.django_db
class TestGlobalCtas:
    """Tests for global_ctas context processor."""

    def test_returns_ctas_key(self, request_obj):
        """Test that result contains 'ctas' key."""
        result = global_ctas(request_obj)
        assert 'ctas' in result

    def test_includes_active_statistic(self, request_obj, site_statistic):
        """Test that active site statistics appear in queryset."""
        result = global_ctas(request_obj)
        assert site_statistic in result['ctas']


@pytest.mark.django_db
class TestGlobalPages:
    """Tests for global_pages context processor."""

    def test_returns_pages_key(self, request_obj):
        """Test that result contains 'pages' key."""
        result = global_pages(request_obj)
        assert 'pages' in result

    def test_includes_active_plan(self, request_obj, pricing_plan):
        """Test that active pricing plans appear in queryset."""
        result = global_pages(request_obj)
        assert pricing_plan in result['pages']


@pytest.mark.django_db
class TestGlobalContacts:
    """Tests for global_contacts context processor."""

    def test_returns_contacts_key(self, request_obj):
        """Test that result contains 'contacts' key."""
        result = global_contacts(request_obj)
        assert 'contacts' in result

    def test_includes_active_contact(self, request_obj, contact_info):
        """Test that active contact info entries appear in queryset."""
        result = global_contacts(request_obj)
        assert contact_info in result['contacts']


# =============================================================================
# SITE CONFIG - COVERS LINES 56-57 (except block)
# =============================================================================


@pytest.mark.django_db
class TestSiteConfig:
    """Tests for site_config context processor."""

    def test_returns_config_keys(self, request_obj, site_configuration):
        """Test that result contains expected keys when config exists."""
        result = site_config(request_obj)
        assert 'site_name' in result
        assert 'site_config' in result
        assert 'copyright_year' in result

    def test_returns_config_values(self, request_obj, site_configuration):
        """Test that returned values match the singleton configuration."""
        result = site_config(request_obj)
        assert result['site_name'] == site_configuration.site_name
        assert result['site_config'] == site_configuration

    def test_exception_returns_defaults(self, request_obj):
        """Test that an exception in get_solo returns safe defaults.

        Covers lines 56-57: the except Exception block.
        """
        with patch(
            'core.models.SiteConfiguration.get_solo',
            side_effect=Exception('Database unavailable'),
        ):
            result = site_config(request_obj)

        assert result['site_name'] == 'EduPath'
        assert result['site_config'] is None
        assert result['copyright_year'] == '2024'


# =============================================================================
# GLOBAL COURSES - COVERS LINES 73-77 (course_id try/except)
# =============================================================================


@pytest.mark.django_db
class TestGlobalCourses:
    """Tests for global_courses context processor."""

    def test_returns_courses_key(self, request_obj):
        """Test that result contains expected keys."""
        result = global_courses(request_obj)
        assert 'courses' in result
        assert 'selected_course' in result

    def test_no_course_id_selected_is_none(self, request_obj, course):
        """Test that selected_course is None when no course_id given."""
        result = global_courses(request_obj)
        assert result['selected_course'] is None

    def test_valid_course_id_selects_course(self, rf, course):
        """Test that a valid numeric course_id selects the matching course.

        Covers lines 73-75: the try block converting course_id and querying.
        """
        request = rf.get('/', {'course_id': str(course.id)})
        result = global_courses(request)
        assert result['selected_course'] == course

    def test_valid_course_id_no_match(self, rf, course):
        """Test that a valid numeric course_id with no match returns None."""
        request = rf.get('/', {'course_id': '999999'})
        result = global_courses(request)
        assert result['selected_course'] is None

    def test_invalid_course_id_returns_none(self, rf, course):
        """Test that a non-numeric course_id falls through to None.

        Covers lines 76-77: the except (TypeError, ValueError) block.
        """
        request = rf.get('/', {'course_id': 'abc'})
        result = global_courses(request)
        assert result['selected_course'] is None

    def test_includes_active_course(self, request_obj, course):
        """Test that active courses appear in the queryset."""
        result = global_courses(request_obj)
        assert course in result['courses']


# =============================================================================
# GLOBAL INSTRUCTORS
# =============================================================================


@pytest.mark.django_db
class TestGlobalInstructors:
    """Tests for global_instructors context processor."""

    def test_returns_instructors_key(self, request_obj):
        """Test that result contains 'instructors' key."""
        result = global_instructors(request_obj)
        assert 'instructors' in result

    def test_includes_active_instructor(self, request_obj, instructor):
        """Test that active instructors appear in queryset."""
        result = global_instructors(request_obj)
        assert instructor in result['instructors']


# =============================================================================
# GLOBAL CATEGORIES
# =============================================================================


@pytest.mark.django_db
class TestGlobalCategories:
    """Tests for global_categories context processor."""

    def test_returns_categories_key(self, request_obj):
        """Test that result contains 'categories' key."""
        result = global_categories(request_obj)
        assert 'categories' in result

    def test_includes_active_category(self, request_obj, category):
        """Test that active categories are returned by the processor."""
        result = global_categories(request_obj)
        # The Category model has a 'course_count' property that conflicts
        # with the Count annotation, so we verify via values_list instead.
        category_ids = list(result['categories'].values_list('id', flat=True))
        assert category.id in category_ids

    def test_queryset_has_annotation(self, request_obj, category):
        """Test that the queryset includes the Count annotation in its query."""
        result = global_categories(request_obj)
        qs = result['categories']
        # Verify the annotation is present in the queryset's query
        assert 'course_count' in qs.query.annotations


# =============================================================================
# GLOBAL REVIEWS
# =============================================================================


@pytest.mark.django_db
class TestGlobalReviews:
    """Tests for global_reviews context processor."""

    def test_returns_reviews_key(self, request_obj):
        """Test that result contains 'reviews' key."""
        result = global_reviews(request_obj)
        assert 'reviews' in result

    def test_includes_active_review(self, request_obj, review):
        """Test that active reviews appear in queryset."""
        result = global_reviews(request_obj)
        assert review in result['reviews']


# =============================================================================
# GLOBAL BLOGS - COVERS LINES 114-118 (blog_id try/except)
# =============================================================================


@pytest.mark.django_db
class TestGlobalBlogs:
    """Tests for global_blogs context processor."""

    def test_returns_blogs_key(self, request_obj):
        """Test that result contains expected keys."""
        result = global_blogs(request_obj)
        assert 'blogs' in result
        assert 'selected_blog' in result

    def test_no_blog_id_selected_is_none(self, request_obj, blog):
        """Test that selected_blog is None when no blog_id given."""
        result = global_blogs(request_obj)
        assert result['selected_blog'] is None

    def test_valid_blog_id_selects_blog(self, rf, blog):
        """Test that a valid numeric blog_id selects the matching blog.

        Covers lines 114-116: the try block converting blog_id and querying.
        """
        request = rf.get('/', {'blog_id': str(blog.id)})
        result = global_blogs(request)
        assert result['selected_blog'] == blog

    def test_valid_blog_id_no_match(self, rf, blog):
        """Test that a valid numeric blog_id with no match returns None."""
        request = rf.get('/', {'blog_id': '999999'})
        result = global_blogs(request)
        assert result['selected_blog'] is None

    def test_invalid_blog_id_returns_none(self, rf, blog):
        """Test that a non-numeric blog_id falls through to None.

        Covers lines 117-118: the except (TypeError, ValueError) block.
        """
        request = rf.get('/', {'blog_id': 'xyz'})
        result = global_blogs(request)
        assert result['selected_blog'] is None

    def test_includes_active_blog(self, request_obj, blog):
        """Test that active blogs appear in the queryset."""
        result = global_blogs(request_obj)
        assert blog in result['blogs']


# =============================================================================
# COURSE VARIANT PROCESSORS
# =============================================================================


@pytest.mark.django_db
class TestGlobalCourses1:
    """Tests for global_courses1 context processor (YouTube video courses)."""

    def test_returns_courses1_key(self, request_obj):
        """Test that result contains 'courses1' key."""
        result = global_courses1(request_obj)
        assert 'courses1' in result

    def test_excludes_courses_without_video_url(self, request_obj, course):
        """Test that courses without video_url are excluded."""
        result = global_courses1(request_obj)
        assert course not in result['courses1']


@pytest.mark.django_db
class TestGlobalCourses2:
    """Tests for global_courses2 context processor (local video courses)."""

    def test_returns_courses2_key(self, request_obj):
        """Test that result contains 'courses2' key."""
        result = global_courses2(request_obj)
        assert 'courses2' in result


@pytest.mark.django_db
class TestGlobalCourses3:
    """Tests for global_courses3 context processor (featured courses)."""

    def test_returns_courses3_key(self, request_obj):
        """Test that result contains 'courses3' key."""
        result = global_courses3(request_obj)
        assert 'courses3' in result

    def test_includes_featured_course(self, request_obj, course):
        """Test that featured active courses appear in queryset."""
        result = global_courses3(request_obj)
        assert course in result['courses3']


# =============================================================================
# USER INFO
# =============================================================================


@pytest.mark.django_db
class TestUserInfo:
    """Tests for user_info context processor."""

    def test_authenticated_user_returns_info(self, rf, user):
        """Test that an authenticated user gets full_name and email."""
        request = rf.get('/')
        request.user = user
        result = user_info(request)
        assert result['user_full_name'] == 'Test User'
        assert result['user_email'] == 'testuser@example.com'

    def test_anonymous_user_returns_empty(self, rf):
        """Test that an anonymous user gets an empty dict."""
        from django.contrib.auth.models import AnonymousUser
        request = rf.get('/')
        request.user = AnonymousUser()
        result = user_info(request)
        assert result == {}

    def test_user_without_name_uses_username(self, rf, db):
        """Test fallback to username when first/last name are empty."""
        from django.contrib.auth.models import User
        nameless_user = User.objects.create_user(
            username='nameless',
            email='nameless@example.com',
            password='pass123',
        )
        request = rf.get('/')
        request.user = nameless_user
        result = user_info(request)
        assert result['user_full_name'] == 'nameless'
