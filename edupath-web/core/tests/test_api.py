"""
Tests for core API views.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestFeatureViewSet:
    """Tests for FeatureViewSet."""

    def test_feature_list(self, api_client, feature):
        """Test listing features."""
        url = '/core/api/v1/features/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestBusinessPartnerViewSet:
    """Tests for BusinessPartnerViewSet."""

    def test_business_partner_list(self, api_client, business_partner):
        """Test listing business partners."""
        url = '/core/api/v1/business-partners/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestSiteStatisticViewSet:
    """Tests for SiteStatisticViewSet."""

    def test_site_statistic_list(self, api_client, site_statistic):
        """Test listing site statistics."""
        url = '/core/api/v1/statistics/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPricingPlanViewSet:
    """Tests for PricingPlanViewSet."""

    def test_pricing_plan_list(self, api_client, pricing_plan):
        """Test listing pricing plans."""
        url = '/core/api/v1/pricing-plans/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestContactInfoViewSet:
    """Tests for ContactInfoViewSet."""

    def test_contact_info_list(self, api_client, contact_info):
        """Test listing contact info."""
        url = '/core/api/v1/contact-info/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestContactSubmissionAPIView:
    """Tests for ContactSubmissionAPIView."""

    def test_contact_submission_post_success(self, api_client):
        """Test creating contact submission."""
        url = '/core/api/v1/contact/'
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'message' in response.data

    def test_contact_submission_post_invalid(self, api_client):
        """Test contact submission with invalid data."""
        url = '/core/api/v1/contact/'
        data = {
            'name': 'John Doe',
            # Missing required fields
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contact_submission_email_validation(self, api_client):
        """Test contact submission email validation."""
        url = '/core/api/v1/contact/'
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test',
            'message': 'Test'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_contact_submission_authenticated_links_user(self, authenticated_client, user):
        """Test that authenticated user is linked to contact submission."""
        url = '/core/api/v1/contact/'
        data = {
            'name': 'Auth User',
            'email': 'auth@example.com',
            'subject': 'Auth Test',
            'message': 'Testing with auth'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        from core.models import ContactSubmission
        submission = ContactSubmission.objects.get(email='auth@example.com')
        assert submission.user == user


@pytest.mark.django_db
class TestSiteConfigurationAPIView:
    """Tests for SiteConfigurationAPIView."""

    def test_site_configuration_get(self, api_client, site_configuration):
        """Test getting site configuration."""
        url = '/core/api/v1/site-config/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'site_name' in response.data


@pytest.mark.django_db
class TestHomepageDataAPIView:
    """Tests for HomepageDataAPIView."""

    def test_homepage_data_get(self, api_client, feature, business_partner, category, course, instructor, site_statistic, blog):
        """Test getting combined homepage data."""
        url = '/core/api/v1/homepage/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'features' in response.data
        assert 'business_partners' in response.data
        assert 'categories' in response.data
        assert 'featured_courses' in response.data
        assert 'instructors' in response.data
        assert 'statistics' in response.data
        assert 'recent_blogs' in response.data

    def test_homepage_data_empty(self, api_client, db):
        """Test homepage data with empty database."""
        url = '/core/api/v1/homepage/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Should return empty lists, not error
        assert response.data['features'] == []
