"""
Pytest Configuration and Fixtures for EduPath Tests.

This module provides shared fixtures for all test modules:
- API client fixtures (authenticated, admin)
- Database fixtures (users, profiles)
- Factory fixtures
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


# =============================================================================
# SETTINGS OVERRIDES FOR TESTING
# =============================================================================

@pytest.fixture(autouse=True)
def _disable_ssl_redirect(settings):
    """Disable SECURE_SSL_REDIRECT during tests to prevent 301 redirects."""
    settings.SECURE_SSL_REDIRECT = False


# =============================================================================
# API CLIENT FIXTURES
# =============================================================================

@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a regular user for testing."""
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User'
    )
    return admin


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an API client authenticated as a regular user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an API client authenticated as an admin."""
    api_client.force_authenticate(user=admin_user)
    return api_client


# =============================================================================
# DJANGO CLIENT FIXTURES
# =============================================================================

@pytest.fixture
def logged_in_client(client, user):
    """Return a Django test client logged in as a regular user."""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def admin_logged_in_client(client, admin_user):
    """Return a Django test client logged in as an admin."""
    client.login(username='admin', password='adminpass123')
    return client


# =============================================================================
# MODEL FIXTURES
# =============================================================================

@pytest.fixture
def user_profile(user):
    """Return the user's profile (created via signal)."""
    from accounts.models import UserProfile
    # Profile should be created automatically via signal
    return UserProfile.objects.get(user=user)


@pytest.fixture
def category(db):
    """Create a test category."""
    from courses.models import Category
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        icon='uil uil-test',
        description='A test category',
        is_active=True
    )


@pytest.fixture
def instructor(db):
    """Create a test instructor."""
    from courses.models import Instructor
    return Instructor.objects.create(
        name='Test Instructor',
        slug='test-instructor',
        title='Senior Developer',
        bio='An experienced instructor',
        is_active=True
    )


@pytest.fixture
def course(db, category, instructor):
    """Create a test course."""
    from courses.models import Course
    return Course.objects.create(
        title='Test Course',
        slug='test-course',
        desc='A test course description',
        price='49.99',
        category=category,
        instructor=instructor,
        lessons=10,
        students=100,
        is_active=True,
        is_featured=True
    )


@pytest.fixture
def review(db, user, course):
    """Create a test review."""
    from courses.models import Review
    return Review.objects.create(
        name=user.get_full_name() or user.username,
        title='Student',
        desc='Great course!',
        rating=5,
        user=user,
        course=course,
        is_active=True
    )


@pytest.fixture
def blog(db, instructor):
    """Create a test blog post."""
    from blog.models import Blog
    return Blog.objects.create(
        title='Test Blog Post',
        slug='test-blog-post',
        name='Development',
        content='This is test blog content.',
        excerpt='Test excerpt',
        author=instructor,
        is_active=True
    )


@pytest.fixture
def feature(db):
    """Create a test feature."""
    from core.models import Feature
    return Feature.objects.create(
        icon='uil uil-test',
        title='Test Feature',
        desc='A test feature description',
        is_active=True
    )


@pytest.fixture
def business_partner(db):
    """Create a test business partner."""
    from core.models import BusinessPartner
    return BusinessPartner.objects.create(
        name='Test Partner',
        img='assets/images/partner.png',
        website_url='https://example.com',
        is_active=True
    )


@pytest.fixture
def site_statistic(db):
    """Create a test site statistic."""
    from core.models import SiteStatistic
    return SiteStatistic.objects.create(
        title='Courses',
        number=0,
        target=100,
        symbol='+',
        is_active=True
    )


@pytest.fixture
def pricing_plan(db):
    """Create a test pricing plan."""
    from core.models import PricingPlan
    return PricingPlan.objects.create(
        name='Monthly',
        price='29.99',
        duration='Month',
        button_text='Subscribe',
        features=['Feature 1', 'Feature 2'],
        is_active=True
    )


@pytest.fixture
def contact_info(db):
    """Create a test contact info."""
    from core.models import ContactInfo
    return ContactInfo.objects.create(
        icon='uil uil-phone',
        name='Phone',
        title='Call us anytime',
        info='+1 234 567 890',
        is_active=True
    )


@pytest.fixture
def contact_submission(db, user):
    """Create a test contact submission."""
    from core.models import ContactSubmission
    return ContactSubmission.objects.create(
        name='Test User',
        email='test@example.com',
        subject='Test Subject',
        message='Test message content',
        user=user
    )


@pytest.fixture
def site_configuration(db):
    """Get or create the site configuration singleton."""
    from core.models import SiteConfiguration
    return SiteConfiguration.get_solo()
