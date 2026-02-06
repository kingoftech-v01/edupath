"""
Core Serializers - API serializers for core app.
"""

from rest_framework import serializers
from .models import (
    Feature, BusinessPartner, SiteStatistic, PricingPlan,
    ContactInfo, ContactSubmission, SiteConfiguration
)


class FeatureSerializer(serializers.ModelSerializer):
    """
    Feature serializer.

    Serializes platform features for homepage display.
    """

    class Meta:
        model = Feature
        fields = ['id', 'icon', 'title', 'desc', 'link_url']


class BusinessPartnerSerializer(serializers.ModelSerializer):
    """
    Business partner serializer.

    Serializes partner logos for carousel display.
    """

    class Meta:
        model = BusinessPartner
        fields = ['id', 'name', 'img', 'website_url']


class SiteStatisticSerializer(serializers.ModelSerializer):
    """
    Site statistic serializer.

    Serializes statistics for animated counter display.
    """

    class Meta:
        model = SiteStatistic
        fields = ['id', 'title', 'number', 'target', 'symbol']


class PricingPlanSerializer(serializers.ModelSerializer):
    """
    Pricing plan serializer.

    Serializes pricing plans including features list and styling.
    """

    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'price', 'duration', 'button_text',
            'style', 'button_style', 'features'
        ]


class ContactInfoSerializer(serializers.ModelSerializer):
    """
    Contact info serializer.

    Serializes contact methods for contact page display.
    """

    class Meta:
        model = ContactInfo
        fields = ['id', 'icon', 'name', 'title', 'info', 'link_url']


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """
    Contact submission serializer for form submissions.

    Handles contact form creation with optional user linking.
    """

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

    def create(self, validated_data):
        """
        Create contact submission with optional user link.

        Links submission to authenticated user if available.

        Args:
            validated_data: Validated form data.

        Returns:
            ContactSubmission: Created submission instance.
        """
        # Link submission to user account if logged in, enabling reply/follow-up.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class SiteConfigurationSerializer(serializers.ModelSerializer):
    """
    Site configuration serializer.

    Serializes the singleton site configuration. Excludes ID
    since it's always 1 and adds no value to API consumers.
    """

    class Meta:
        model = SiteConfiguration
        # Exclude id since it's always 1 (singleton) and adds no value to API consumers.
        exclude = ['id']
