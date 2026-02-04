"""
Tests for the migrate_static_data management command.
"""

import pytest
from io import StringIO

from django.core.management import call_command

from core.models import (
    SiteConfiguration, Feature, BusinessPartner,
    SiteStatistic, ContactInfo, PricingPlan
)
from courses.models import Category, Instructor, Course, Review
from blog.models import Blog

from core.management.commands.migrate_static_data import Command


def _make_command(out=None):
    """Create a Command instance with captured stdout."""
    if out is None:
        out = StringIO()
    return Command(stdout=out), out


# =============================================================================
# FULL COMMAND TESTS
# =============================================================================

@pytest.mark.django_db
class TestMigrateStaticDataFullRun:
    """Tests for running the full migrate_static_data command."""

    def test_command_from_scratch(self):
        """Test running the command on an empty database creates all expected data."""
        out = StringIO()
        call_command('migrate_static_data', stdout=out)
        output = out.getvalue()

        assert 'Starting data migration' in output
        assert 'Data migration completed successfully' in output

        assert SiteConfiguration.objects.count() == 1
        assert Feature.objects.count() == 4
        assert BusinessPartner.objects.count() == 6
        assert SiteStatistic.objects.count() == 4
        assert ContactInfo.objects.count() == 3
        assert PricingPlan.objects.count() == 3
        assert Category.objects.count() == 8
        assert Instructor.objects.count() == 8
        assert Course.objects.count() == 12
        assert Review.objects.count() == 6
        assert Blog.objects.count() == 9

    def test_command_idempotent(self):
        """Test running the command twice does not duplicate any data."""
        out1 = StringIO()
        call_command('migrate_static_data', stdout=out1)

        counts_after_first_run = {
            'site_config': SiteConfiguration.objects.count(),
            'features': Feature.objects.count(),
            'partners': BusinessPartner.objects.count(),
            'statistics': SiteStatistic.objects.count(),
            'contacts': ContactInfo.objects.count(),
            'plans': PricingPlan.objects.count(),
            'categories': Category.objects.count(),
            'instructors': Instructor.objects.count(),
            'courses': Course.objects.count(),
            'reviews': Review.objects.count(),
            'blogs': Blog.objects.count(),
        }

        out2 = StringIO()
        call_command('migrate_static_data', stdout=out2)

        assert SiteConfiguration.objects.count() == counts_after_first_run['site_config']
        assert Feature.objects.count() == counts_after_first_run['features']
        assert BusinessPartner.objects.count() == counts_after_first_run['partners']
        assert SiteStatistic.objects.count() == counts_after_first_run['statistics']
        assert ContactInfo.objects.count() == counts_after_first_run['contacts']
        assert PricingPlan.objects.count() == counts_after_first_run['plans']
        assert Category.objects.count() == counts_after_first_run['categories']
        assert Instructor.objects.count() == counts_after_first_run['instructors']
        assert Course.objects.count() == counts_after_first_run['courses']
        assert Review.objects.count() == counts_after_first_run['reviews']
        assert Blog.objects.count() == counts_after_first_run['blogs']

    def test_second_run_output_shows_existing(self):
        """Test that the second run output reflects that data already exists."""
        out1 = StringIO()
        call_command('migrate_static_data', stdout=out1)

        out2 = StringIO()
        call_command('migrate_static_data', stdout=out2)
        output = out2.getvalue()

        # Site config should indicate it already exists
        assert 'already exists' in output
        # Other models should report 0 created
        assert '0 created' in output


# =============================================================================
# CREATE SITE CONFIG TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateSiteConfig:
    """Tests for the create_site_config method."""

    def test_creates_site_configuration(self):
        """Test that site configuration is created with correct data."""
        cmd, _ = _make_command()
        cmd.create_site_config()

        config = SiteConfiguration.objects.get(pk=1)
        assert config.site_name == 'EduPath'
        assert config.tagline == 'Learn Without Limits'
        assert config.facebook_url == 'https://facebook.com/edupath'
        assert config.twitter_url == 'https://twitter.com/edupath'
        assert config.linkedin_url == 'https://linkedin.com/company/edupath'
        assert config.instagram_url == 'https://instagram.com/edupath'
        assert config.youtube_url == 'https://youtube.com/edupath'
        assert config.copyright_text == '\u00a9 2024 EduPath. All rights reserved.'

    def test_does_not_overwrite_existing_config_with_name(self):
        """Test that an existing config with a site_name is not overwritten."""
        SiteConfiguration.objects.create(pk=1, site_name='Custom Site')

        cmd, _ = _make_command()
        cmd.create_site_config()

        config = SiteConfiguration.objects.get(pk=1)
        assert config.site_name == 'Custom Site'

    def test_populates_config_when_site_name_is_blank(self):
        """Test that a config with blank site_name gets populated."""
        SiteConfiguration.objects.create(pk=1, site_name='')

        cmd, _ = _make_command()
        cmd.create_site_config()

        config = SiteConfiguration.objects.get(pk=1)
        assert config.site_name == 'EduPath'

    def test_output_on_creation(self):
        """Test stdout message when config is newly created."""
        cmd, out = _make_command()
        cmd.create_site_config()

        assert 'Site configuration created' in out.getvalue()

    def test_output_when_already_exists(self):
        """Test stdout message when config already exists."""
        SiteConfiguration.objects.create(pk=1, site_name='Existing')

        cmd, out = _make_command()
        cmd.create_site_config()

        assert 'already exists' in out.getvalue()

    def test_idempotent(self):
        """Test that calling create_site_config twice keeps exactly one config."""
        cmd, _ = _make_command()
        cmd.create_site_config()
        cmd.create_site_config()

        assert SiteConfiguration.objects.count() == 1


# =============================================================================
# CREATE FEATURES TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateFeatures:
    """Tests for the create_features method."""

    def test_creates_four_features(self):
        """Test that exactly four features are created."""
        cmd, _ = _make_command()
        cmd.create_features()

        assert Feature.objects.count() == 4

    def test_feature_titles(self):
        """Test that features have the expected titles."""
        cmd, _ = _make_command()
        cmd.create_features()

        titles = set(Feature.objects.values_list('title', flat=True))
        expected = {'Digital Marketing', 'Photography', 'Development', 'Music & Audio'}
        assert titles == expected

    def test_features_have_icons(self):
        """Test that every feature has an icon class set."""
        cmd, _ = _make_command()
        cmd.create_features()

        for feature in Feature.objects.all():
            assert feature.icon != ''
            assert 'uil' in feature.icon

    def test_features_have_link_urls(self):
        """Test that every feature has a link_url."""
        cmd, _ = _make_command()
        cmd.create_features()

        for feature in Feature.objects.all():
            assert feature.link_url.startswith('/courses/')

    def test_features_have_sequential_order(self):
        """Test that features are assigned sequential order values."""
        cmd, _ = _make_command()
        cmd.create_features()

        orders = list(Feature.objects.order_by('order').values_list('order', flat=True))
        assert orders == [1, 2, 3, 4]

    def test_idempotent(self):
        """Test that calling create_features twice does not create duplicates."""
        cmd, _ = _make_command()
        cmd.create_features()
        cmd.create_features()

        assert Feature.objects.count() == 4

    def test_output_first_run(self):
        """Test output shows all features created on first run."""
        cmd, out = _make_command()
        cmd.create_features()

        assert '4 created' in out.getvalue()
        assert '0 existed' in out.getvalue()

    def test_output_second_run(self):
        """Test output shows all features existed on second run."""
        cmd, _ = _make_command()
        cmd.create_features()

        cmd2, out2 = _make_command()
        cmd2.create_features()

        assert '0 created' in out2.getvalue()
        assert '4 existed' in out2.getvalue()


# =============================================================================
# CREATE BUSINESS PARTNERS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateBusinessPartners:
    """Tests for the create_business_partners method."""

    def test_creates_six_partners(self):
        """Test that exactly six business partners are created."""
        cmd, _ = _make_command()
        cmd.create_business_partners()

        assert BusinessPartner.objects.count() == 6

    def test_partner_names(self):
        """Test that partners have the expected names."""
        cmd, _ = _make_command()
        cmd.create_business_partners()

        names = set(BusinessPartner.objects.values_list('name', flat=True))
        expected = {'Amazon', 'Google', 'LinkedIn', 'Facebook', 'Spotify', 'Shopify'}
        assert names == expected

    def test_partners_have_images(self):
        """Test that every partner has an image path."""
        cmd, _ = _make_command()
        cmd.create_business_partners()

        for partner in BusinessPartner.objects.all():
            assert partner.img != ''
            assert 'assets/images/client/' in partner.img

    def test_partners_have_website_urls(self):
        """Test that every partner has a website URL."""
        cmd, _ = _make_command()
        cmd.create_business_partners()

        for partner in BusinessPartner.objects.all():
            assert partner.website_url.startswith('https://')

    def test_idempotent(self):
        """Test that calling create_business_partners twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_business_partners()
        cmd.create_business_partners()

        assert BusinessPartner.objects.count() == 6


# =============================================================================
# CREATE STATISTICS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateStatistics:
    """Tests for the create_statistics method."""

    def test_creates_four_statistics(self):
        """Test that exactly four statistics are created."""
        cmd, _ = _make_command()
        cmd.create_statistics()

        assert SiteStatistic.objects.count() == 4

    def test_statistic_titles(self):
        """Test that statistics have the expected titles."""
        cmd, _ = _make_command()
        cmd.create_statistics()

        titles = set(SiteStatistic.objects.values_list('title', flat=True))
        expected = {'Courses', 'Countries', 'Students', 'Instructors'}
        assert titles == expected

    def test_statistics_start_at_zero(self):
        """Test that all statistics start at number zero."""
        cmd, _ = _make_command()
        cmd.create_statistics()

        for stat in SiteStatistic.objects.all():
            assert stat.number == 0

    def test_statistics_have_positive_targets(self):
        """Test that all statistics have a target greater than zero."""
        cmd, _ = _make_command()
        cmd.create_statistics()

        for stat in SiteStatistic.objects.all():
            assert stat.target > 0

    def test_statistics_have_symbols(self):
        """Test that every statistic has a symbol."""
        cmd, _ = _make_command()
        cmd.create_statistics()

        for stat in SiteStatistic.objects.all():
            assert stat.symbol in ('+', 'K')

    def test_idempotent(self):
        """Test that calling create_statistics twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_statistics()
        cmd.create_statistics()

        assert SiteStatistic.objects.count() == 4


# =============================================================================
# CREATE CONTACT INFO TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateContactInfo:
    """Tests for the create_contact_info method."""

    def test_creates_three_contacts(self):
        """Test that exactly three contact info entries are created."""
        cmd, _ = _make_command()
        cmd.create_contact_info()

        assert ContactInfo.objects.count() == 3

    def test_contact_names(self):
        """Test that contacts have the expected names."""
        cmd, _ = _make_command()
        cmd.create_contact_info()

        names = set(ContactInfo.objects.values_list('name', flat=True))
        expected = {'Phone', 'Email', 'Location'}
        assert names == expected

    def test_phone_contact_details(self):
        """Test that the phone contact has correct details."""
        cmd, _ = _make_command()
        cmd.create_contact_info()

        phone = ContactInfo.objects.get(name='Phone')
        assert phone.info == '+1 234-567-8900'
        assert phone.link_url == 'tel:+12345678900'
        assert 'uil uil-phone' in phone.icon

    def test_email_contact_details(self):
        """Test that the email contact has correct details."""
        cmd, _ = _make_command()
        cmd.create_contact_info()

        email = ContactInfo.objects.get(name='Email')
        assert email.info == 'contact@edupath.com'
        assert email.link_url == 'mailto:contact@edupath.com'

    def test_location_contact_details(self):
        """Test that the location contact has correct details."""
        cmd, _ = _make_command()
        cmd.create_contact_info()

        location = ContactInfo.objects.get(name='Location')
        assert 'New York' in location.info

    def test_idempotent(self):
        """Test that calling create_contact_info twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_contact_info()
        cmd.create_contact_info()

        assert ContactInfo.objects.count() == 3


# =============================================================================
# CREATE PRICING PLANS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreatePricingPlans:
    """Tests for the create_pricing_plans method."""

    def test_creates_three_plans(self):
        """Test that exactly three pricing plans are created."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        assert PricingPlan.objects.count() == 3

    def test_plan_names_and_durations(self):
        """Test that plans have correct name-duration pairs."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        plans = {p.name: p.duration for p in PricingPlan.objects.all()}
        assert plans['Weekly'] == 'Week'
        assert plans['Monthly'] == 'Month'
        assert plans['Yearly'] == 'Year'

    def test_plan_prices(self):
        """Test that plans have the expected prices."""
        from decimal import Decimal

        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        prices = {p.name: p.price for p in PricingPlan.objects.all()}
        assert prices['Weekly'] == Decimal('9.99')
        assert prices['Monthly'] == Decimal('29.99')
        assert prices['Yearly'] == Decimal('199.99')

    def test_plans_have_features_list(self):
        """Test that each plan has a non-empty features list."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        for plan in PricingPlan.objects.all():
            assert isinstance(plan.features, list)
            assert len(plan.features) > 0

    def test_monthly_plan_has_more_features_than_weekly(self):
        """Test that the Monthly plan has more features than the Weekly plan."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        weekly = PricingPlan.objects.get(name='Weekly')
        monthly = PricingPlan.objects.get(name='Monthly')
        assert len(monthly.features) > len(weekly.features)

    def test_yearly_plan_has_most_features(self):
        """Test that the Yearly plan has the most features."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        yearly = PricingPlan.objects.get(name='Yearly')
        for plan in PricingPlan.objects.exclude(name='Yearly'):
            assert len(yearly.features) > len(plan.features)

    def test_plans_have_button_text(self):
        """Test that each plan has button text."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()

        for plan in PricingPlan.objects.all():
            assert plan.button_text == 'Get Started'

    def test_idempotent(self):
        """Test that calling create_pricing_plans twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_pricing_plans()
        cmd.create_pricing_plans()

        assert PricingPlan.objects.count() == 3


# =============================================================================
# CREATE CATEGORIES TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateCategories:
    """Tests for the create_categories method."""

    def test_creates_eight_categories(self):
        """Test that exactly eight categories are created."""
        cmd, _ = _make_command()
        cmd.create_categories()

        assert Category.objects.count() == 8

    def test_category_slugs(self):
        """Test that categories have the expected slugs."""
        cmd, _ = _make_command()
        cmd.create_categories()

        slugs = set(Category.objects.values_list('slug', flat=True))
        expected = {
            'development', 'business', 'design', 'marketing',
            'photography', 'music', 'health', 'language'
        }
        assert slugs == expected

    def test_category_names(self):
        """Test that categories have the expected names."""
        cmd, _ = _make_command()
        cmd.create_categories()

        names = set(Category.objects.values_list('name', flat=True))
        expected = {
            'Development', 'Business', 'Design', 'Marketing',
            'Photography', 'Music', 'Health', 'Language'
        }
        assert names == expected

    def test_categories_have_icons(self):
        """Test that every category has an icon class."""
        cmd, _ = _make_command()
        cmd.create_categories()

        for cat in Category.objects.all():
            assert cat.icon != ''
            assert 'uil' in cat.icon

    def test_categories_have_descriptions(self):
        """Test that every category has a description."""
        cmd, _ = _make_command()
        cmd.create_categories()

        for cat in Category.objects.all():
            assert cat.description != ''

    def test_categories_have_sequential_order(self):
        """Test that categories have sequential order values."""
        cmd, _ = _make_command()
        cmd.create_categories()

        orders = list(Category.objects.order_by('order').values_list('order', flat=True))
        assert orders == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_idempotent(self):
        """Test that calling create_categories twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_categories()
        cmd.create_categories()

        assert Category.objects.count() == 8


# =============================================================================
# CREATE INSTRUCTORS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateInstructors:
    """Tests for the create_instructors method."""

    def test_creates_eight_instructors(self):
        """Test that exactly eight instructors are created."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        assert Instructor.objects.count() == 8

    def test_instructor_slugs(self):
        """Test that instructors have the expected slugs."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        slugs = set(Instructor.objects.values_list('slug', flat=True))
        expected = {
            'john-smith', 'sarah-johnson', 'michael-chen', 'emily-brown',
            'david-wilson', 'lisa-anderson', 'robert-taylor', 'jennifer-martinez'
        }
        assert slugs == expected

    def test_instructor_names(self):
        """Test that instructors have the expected names."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        names = set(Instructor.objects.values_list('name', flat=True))
        expected = {
            'John Smith', 'Sarah Johnson', 'Michael Chen', 'Emily Brown',
            'David Wilson', 'Lisa Anderson', 'Robert Taylor', 'Jennifer Martinez'
        }
        assert names == expected

    def test_instructors_have_titles(self):
        """Test that every instructor has a professional title."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        for inst in Instructor.objects.all():
            assert inst.title != ''

    def test_instructors_have_bios(self):
        """Test that every instructor has a bio."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        for inst in Instructor.objects.all():
            assert inst.bio != ''

    def test_instructors_have_social_urls(self):
        """Test that every instructor has social media URLs."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        for inst in Instructor.objects.all():
            assert inst.facebook_url != ''
            assert inst.twitter_url != ''
            assert inst.linkedin_url != ''

    def test_instructors_have_images(self):
        """Test that every instructor has an image path."""
        cmd, _ = _make_command()
        cmd.create_instructors()

        for inst in Instructor.objects.all():
            assert 'assets/images/team/' in str(inst.img)

    def test_idempotent(self):
        """Test that calling create_instructors twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_instructors()
        cmd.create_instructors()

        assert Instructor.objects.count() == 8


# =============================================================================
# CREATE COURSES TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateCourses:
    """Tests for the create_courses method."""

    @staticmethod
    def _setup_dependencies(cmd):
        """Create the categories and instructors that courses depend on."""
        cmd.create_categories()
        cmd.create_instructors()

    def test_creates_twelve_courses(self):
        """Test that exactly twelve courses are created."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        assert Course.objects.count() == 12

    def test_every_course_has_a_category(self):
        """Test that every course is linked to a category."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        for course in Course.objects.all():
            assert course.category is not None

    def test_every_course_has_an_instructor(self):
        """Test that every course is linked to an instructor."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        for course in Course.objects.all():
            assert course.instructor is not None

    def test_featured_course_count(self):
        """Test that six courses are marked as featured."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        assert Course.objects.filter(is_featured=True).count() == 6

    def test_non_featured_course_count(self):
        """Test that six courses are not featured."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        assert Course.objects.filter(is_featured=False).count() == 6

    def test_courses_have_prices(self):
        """Test that every course has a positive price."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        for course in Course.objects.all():
            assert course.price > 0

    def test_courses_have_lessons(self):
        """Test that every course has at least one lesson."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        for course in Course.objects.all():
            assert course.lessons > 0

    def test_courses_have_students(self):
        """Test that every course has a positive student count."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        for course in Course.objects.all():
            assert course.students > 0

    def test_course_slugs_are_unique(self):
        """Test that all course slugs are unique."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        slugs = list(Course.objects.values_list('slug', flat=True))
        assert len(slugs) == len(set(slugs))

    def test_some_courses_have_video_urls(self):
        """Test that at least one course has a video URL."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        courses_with_video = Course.objects.exclude(video_url='')
        assert courses_with_video.count() >= 1

    def test_no_courses_created_without_dependencies(self):
        """Test that no courses are created when categories and instructors are missing."""
        cmd, _ = _make_command()
        cmd.create_courses()

        assert Course.objects.count() == 0

    def test_no_courses_created_with_only_categories(self):
        """Test that no courses are created when only categories exist."""
        cmd, _ = _make_command()
        cmd.create_categories()
        cmd.create_courses()

        assert Course.objects.count() == 0

    def test_no_courses_created_with_only_instructors(self):
        """Test that no courses are created when only instructors exist."""
        cmd, _ = _make_command()
        cmd.create_instructors()
        cmd.create_courses()

        assert Course.objects.count() == 0

    def test_courses_span_multiple_categories(self):
        """Test that courses are distributed across multiple categories."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        category_ids = set(Course.objects.values_list('category_id', flat=True))
        assert len(category_ids) > 1

    def test_courses_span_multiple_instructors(self):
        """Test that courses are distributed across multiple instructors."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()

        instructor_ids = set(Course.objects.values_list('instructor_id', flat=True))
        assert len(instructor_ids) > 1

    def test_idempotent(self):
        """Test that calling create_courses twice does not duplicate."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_courses()
        cmd.create_courses()

        assert Course.objects.count() == 12


# =============================================================================
# CREATE REVIEWS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateReviews:
    """Tests for the create_reviews method."""

    def test_creates_six_reviews(self):
        """Test that exactly six reviews are created."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        assert Review.objects.count() == 6

    def test_review_names(self):
        """Test that reviews have the expected reviewer names."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        names = set(Review.objects.values_list('name', flat=True))
        expected = {
            'Alex Turner', 'Maria Garcia', 'James Wilson',
            'Sophie Chen', 'Daniel Brown', 'Emma Davis'
        }
        assert names == expected

    def test_reviews_have_valid_ratings(self):
        """Test that every review has a rating between 1 and 5."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        for review in Review.objects.all():
            assert 1 <= review.rating <= 5

    def test_reviews_have_descriptions(self):
        """Test that every review has a description."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        for review in Review.objects.all():
            assert review.desc != ''

    def test_reviews_have_titles(self):
        """Test that every review has a title."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        for review in Review.objects.all():
            assert review.title != ''

    def test_reviews_have_images(self):
        """Test that every review has an image path."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        for review in Review.objects.all():
            assert 'assets/images/client/' in str(review.img)

    def test_reviews_have_sequential_order(self):
        """Test that reviews have sequential order values."""
        cmd, _ = _make_command()
        cmd.create_reviews()

        orders = list(Review.objects.order_by('order').values_list('order', flat=True))
        assert orders == [1, 2, 3, 4, 5, 6]

    def test_idempotent(self):
        """Test that calling create_reviews twice does not duplicate."""
        cmd, _ = _make_command()
        cmd.create_reviews()
        cmd.create_reviews()

        assert Review.objects.count() == 6


# =============================================================================
# CREATE BLOGS TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateBlogs:
    """Tests for the create_blogs method."""

    @staticmethod
    def _setup_dependencies(cmd):
        """Create the instructors that blogs depend on for authorship."""
        cmd.create_instructors()

    def test_creates_nine_blogs(self):
        """Test that exactly nine blog posts are created."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        assert Blog.objects.count() == 9

    def test_blog_slugs(self):
        """Test that blogs have expected slugs."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        slugs = set(Blog.objects.values_list('slug', flat=True))
        assert '10-tips-effective-online-learning' in slugs
        assert 'future-edtech-2024' in slugs
        assert 'choose-right-online-course' in slugs
        assert 'career-web-development' in slugs
        assert 'soft-skills-tech' in slugs
        assert 'introduction-machine-learning' in slugs
        assert 'design-principles-developers' in slugs
        assert 'remote-work-best-practices' in slugs
        assert 'understanding-seo-basics' in slugs

    def test_blogs_have_titles(self):
        """Test that every blog has a non-empty title."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        for blog in Blog.objects.all():
            assert blog.title != ''

    def test_blogs_have_content(self):
        """Test that every blog has non-empty content."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        for blog in Blog.objects.all():
            assert blog.content != ''

    def test_blogs_have_excerpts(self):
        """Test that every blog has an excerpt."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        for blog in Blog.objects.all():
            assert blog.excerpt != ''

    def test_blogs_have_images(self):
        """Test that every blog has an image path."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        for blog in Blog.objects.all():
            assert 'assets/images/blog/' in str(blog.img)

    def test_blogs_have_author_when_instructors_exist(self):
        """Test that every blog gets an instructor as author."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        for blog in Blog.objects.all():
            assert blog.author is not None

    def test_blogs_created_without_instructors_have_no_author(self):
        """Test that blogs created without instructors have a null author."""
        cmd, _ = _make_command()
        cmd.create_blogs()

        assert Blog.objects.count() == 9
        for blog in Blog.objects.all():
            assert blog.author is None

    def test_blogs_have_sequential_order(self):
        """Test that blogs have sequential order values."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()

        orders = list(Blog.objects.order_by('order').values_list('order', flat=True))
        assert orders == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_idempotent(self):
        """Test that calling create_blogs twice does not duplicate."""
        cmd, _ = _make_command()
        self._setup_dependencies(cmd)
        cmd.create_blogs()
        cmd.create_blogs()

        assert Blog.objects.count() == 9
