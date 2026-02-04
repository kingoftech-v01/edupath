"""
Tests for core models.
"""

import pytest
from decimal import Decimal

from core.models import (
    Feature, BusinessPartner, SiteStatistic, PricingPlan,
    ContactInfo, ContactSubmission, SiteConfiguration
)


@pytest.mark.django_db
class TestFeature:
    """Tests for Feature model."""

    def test_feature_creation(self, feature):
        """Test Feature instance creation."""
        assert feature.title == 'Test Feature'
        assert feature.is_active is True

    def test_feature_str(self, feature):
        """Test Feature string representation."""
        assert str(feature) == 'Test Feature'


@pytest.mark.django_db
class TestBusinessPartner:
    """Tests for BusinessPartner model."""

    def test_business_partner_creation(self, business_partner):
        """Test BusinessPartner instance creation."""
        assert business_partner.name == 'Test Partner'
        assert business_partner.is_active is True

    def test_business_partner_str(self, business_partner):
        """Test BusinessPartner string representation."""
        assert str(business_partner) == 'Test Partner'


@pytest.mark.django_db
class TestSiteStatistic:
    """Tests for SiteStatistic model."""

    def test_site_statistic_creation(self, site_statistic):
        """Test SiteStatistic instance creation."""
        assert site_statistic.title == 'Courses'
        assert site_statistic.is_active is True

    def test_site_statistic_str(self, site_statistic):
        """Test SiteStatistic string representation."""
        result = str(site_statistic)
        assert 'Courses' in result
        assert '+' in result


@pytest.mark.django_db
class TestPricingPlan:
    """Tests for PricingPlan model."""

    def test_pricing_plan_creation(self, pricing_plan):
        """Test PricingPlan instance creation."""
        assert pricing_plan.name == 'Monthly'
        assert pricing_plan.is_active is True

    def test_pricing_plan_str(self, pricing_plan):
        """Test PricingPlan string representation."""
        result = str(pricing_plan)
        assert 'Monthly' in result
        assert '$' in result

    def test_pricing_plan_features_json(self, db):
        """Test PricingPlan features JSONField."""
        plan = PricingPlan.objects.create(
            name='Premium',
            price=Decimal('99.99'),
            duration='Month',
            features=['Feature A', 'Feature B', 'Feature C']
        )
        assert len(plan.features) == 3
        assert 'Feature A' in plan.features


@pytest.mark.django_db
class TestContactInfo:
    """Tests for ContactInfo model."""

    def test_contact_info_creation(self, contact_info):
        """Test ContactInfo instance creation."""
        assert contact_info.name == 'Phone'
        assert contact_info.is_active is True

    def test_contact_info_str(self, contact_info):
        """Test ContactInfo string representation."""
        assert str(contact_info) == 'Phone'


@pytest.mark.django_db
class TestContactSubmission:
    """Tests for ContactSubmission model."""

    def test_contact_submission_creation(self, contact_submission):
        """Test ContactSubmission instance creation."""
        assert contact_submission.name == 'Test User'
        assert contact_submission.status == 'new'

    def test_contact_submission_str(self, contact_submission):
        """Test ContactSubmission string representation."""
        result = str(contact_submission)
        assert 'Test User' in result
        assert 'Test Subject' in result

    def test_contact_submission_status_choices(self, db):
        """Test ContactSubmission status field choices."""
        submission = ContactSubmission.objects.create(
            name='Test',
            email='test@example.com',
            subject='Subject',
            message='Message',
            status='read'
        )
        assert submission.status == 'read'

    def test_contact_submission_user_relation(self, contact_submission, user):
        """Test contact submission can have user."""
        assert contact_submission.user == user

    def test_contact_submission_ordering(self, db):
        """Test submissions ordered by created_at descending."""
        sub1 = ContactSubmission.objects.create(
            name='First',
            email='first@example.com',
            subject='Sub 1',
            message='Msg 1'
        )
        sub2 = ContactSubmission.objects.create(
            name='Second',
            email='second@example.com',
            subject='Sub 2',
            message='Msg 2'
        )
        submissions = list(ContactSubmission.objects.all())
        assert submissions[0] == sub2


@pytest.mark.django_db
class TestSiteConfiguration:
    """Tests for SiteConfiguration model (Singleton)."""

    def test_site_configuration_singleton(self, db):
        """Test SiteConfiguration is a singleton."""
        config1 = SiteConfiguration.get_solo()
        config2 = SiteConfiguration.get_solo()
        assert config1.pk == config2.pk == 1

    def test_site_configuration_defaults(self, site_configuration):
        """Test SiteConfiguration default values."""
        assert site_configuration.site_name == 'EduPath'

    def test_site_configuration_str(self, site_configuration):
        """Test SiteConfiguration string representation."""
        assert str(site_configuration) == 'EduPath'
