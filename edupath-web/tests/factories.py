"""
Factory Boy Factories for EduPath Test Data Generation.

Usage:
    from tests.factories import UserFactory, CourseFactory

    user = UserFactory()
    course = CourseFactory(price='0.00')  # Free course
"""

import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


# =============================================================================
# USER FACTORIES
# =============================================================================

class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class AdminUserFactory(UserFactory):
    """Factory for creating admin User instances."""

    username = factory.Sequence(lambda n: f'admin{n}')
    is_staff = True
    is_superuser = True


class UserProfileFactory(DjangoModelFactory):
    """Factory for creating UserProfile instances."""

    class Meta:
        model = 'accounts.UserProfile'

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('paragraph')
    phone = factory.Faker('phone_number')
    website = factory.Faker('url')


# =============================================================================
# COURSES FACTORIES
# =============================================================================

class CategoryFactory(DjangoModelFactory):
    """Factory for creating Category instances."""

    class Meta:
        model = 'courses.Category'

    name = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    icon = 'uil uil-book'
    description = factory.Faker('paragraph')
    is_active = True
    order = factory.Sequence(lambda n: n)


class InstructorFactory(DjangoModelFactory):
    """Factory for creating Instructor instances."""

    class Meta:
        model = 'courses.Instructor'

    name = factory.Faker('name')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-').replace('.', ''))
    title = factory.Faker('job')
    bio = factory.Faker('paragraph')
    facebook_url = 'https://facebook.com'
    twitter_url = 'https://twitter.com'
    linkedin_url = 'https://linkedin.com'
    is_active = True
    order = factory.Sequence(lambda n: n)


class CourseFactory(DjangoModelFactory):
    """Factory for creating Course instances."""

    class Meta:
        model = 'courses.Course'

    title = factory.Sequence(lambda n: f'Course {n}')
    slug = factory.LazyAttribute(lambda obj: obj.title.lower().replace(' ', '-'))
    name = factory.LazyAttribute(lambda obj: obj.instructor.name if obj.instructor else 'Instructor')
    desc = factory.Faker('paragraph')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)
    instructor = factory.SubFactory(InstructorFactory)
    lessons = factory.Faker('random_int', min=5, max=50)
    students = factory.Faker('random_int', min=10, max=1000)
    duration_hours = factory.Faker('random_int', min=1, max=20)
    is_active = True
    is_featured = False
    order = factory.Sequence(lambda n: n)


class ReviewFactory(DjangoModelFactory):
    """Factory for creating Review instances."""

    class Meta:
        model = 'courses.Review'

    name = factory.Faker('name')
    title = 'Student'
    desc = factory.Faker('paragraph')
    rating = factory.Faker('random_int', min=1, max=5)
    course = factory.SubFactory(CourseFactory)
    is_active = True
    order = factory.Sequence(lambda n: n)


# =============================================================================
# BLOG FACTORIES
# =============================================================================

class BlogFactory(DjangoModelFactory):
    """Factory for creating Blog instances."""

    class Meta:
        model = 'blog.Blog'

    title = factory.Sequence(lambda n: f'Blog Post {n}')
    slug = factory.LazyAttribute(lambda obj: obj.title.lower().replace(' ', '-'))
    name = factory.Faker('word')
    content = factory.Faker('paragraphs', nb=3)
    excerpt = factory.Faker('sentence')
    author = factory.SubFactory(InstructorFactory)
    read_time_minutes = factory.Faker('random_int', min=3, max=15)
    is_active = True
    order = factory.Sequence(lambda n: n)


# =============================================================================
# CORE FACTORIES
# =============================================================================

class FeatureFactory(DjangoModelFactory):
    """Factory for creating Feature instances."""

    class Meta:
        model = 'core.Feature'

    icon = 'uil uil-star'
    title = factory.Sequence(lambda n: f'Feature {n}')
    desc = factory.Faker('paragraph')
    link_url = factory.Faker('url')
    is_active = True
    order = factory.Sequence(lambda n: n)


class BusinessPartnerFactory(DjangoModelFactory):
    """Factory for creating BusinessPartner instances."""

    class Meta:
        model = 'core.BusinessPartner'

    name = factory.Faker('company')
    img = 'assets/images/partner.png'
    website_url = factory.Faker('url')
    is_active = True
    order = factory.Sequence(lambda n: n)


class SiteStatisticFactory(DjangoModelFactory):
    """Factory for creating SiteStatistic instances."""

    class Meta:
        model = 'core.SiteStatistic'

    title = factory.Sequence(lambda n: f'Statistic {n}')
    number = 0
    target = factory.Faker('random_int', min=10, max=100)
    symbol = '+'
    is_active = True
    order = factory.Sequence(lambda n: n)


class PricingPlanFactory(DjangoModelFactory):
    """Factory for creating PricingPlan instances."""

    class Meta:
        model = 'core.PricingPlan'

    name = factory.Iterator(['Weekly', 'Monthly', 'Yearly'])
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    duration = factory.Iterator(['Week', 'Month', 'Year'])
    button_text = 'Subscribe'
    features = ['Feature 1', 'Feature 2', 'Feature 3']
    is_active = True
    order = factory.Sequence(lambda n: n)


class ContactInfoFactory(DjangoModelFactory):
    """Factory for creating ContactInfo instances."""

    class Meta:
        model = 'core.ContactInfo'

    icon = 'uil uil-phone'
    name = factory.Iterator(['Phone', 'Email', 'Location'])
    title = factory.Faker('sentence')
    info = factory.Faker('phone_number')
    link_url = factory.Faker('url')
    is_active = True
    order = factory.Sequence(lambda n: n)


class ContactSubmissionFactory(DjangoModelFactory):
    """Factory for creating ContactSubmission instances."""

    class Meta:
        model = 'core.ContactSubmission'

    name = factory.Faker('name')
    email = factory.Faker('email')
    subject = factory.Faker('sentence')
    message = factory.Faker('paragraph')
    status = 'new'


class SiteConfigurationFactory(DjangoModelFactory):
    """Factory for creating SiteConfiguration instances."""

    class Meta:
        model = 'core.SiteConfiguration'
        django_get_or_create = ('pk',)

    pk = 1
    site_name = 'EduPath'
    tagline = 'Learn Without Limits'
    facebook_url = 'https://facebook.com/edupath'
    twitter_url = 'https://twitter.com/edupath'
    linkedin_url = 'https://linkedin.com/edupath'
