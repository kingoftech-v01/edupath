"""
Core Serializers - API serializers for core app.
"""

from rest_framework import serializers
from .models import (
    Feature, BusinessPartner, SiteStatistic, PricingPlan,
    ContactInfo, ContactSubmission, SiteConfiguration
)


class FeatureSerializer(serializers.ModelSerializer):
    """Feature serializer."""

    class Meta:
        model = Feature
        fields = ['id', 'icon', 'title', 'desc', 'link_url']


class BusinessPartnerSerializer(serializers.ModelSerializer):
    """Business partner serializer."""

    class Meta:
        model = BusinessPartner
        fields = ['id', 'name', 'img', 'website_url']


class SiteStatisticSerializer(serializers.ModelSerializer):
    """Site statistic serializer."""

    class Meta:
        model = SiteStatistic
        fields = ['id', 'title', 'number', 'target', 'symbol']


class PricingPlanSerializer(serializers.ModelSerializer):
    """Pricing plan serializer."""

    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'price', 'duration', 'button_text',
            'style', 'button_style', 'features'
        ]


class ContactInfoSerializer(serializers.ModelSerializer):
    """Contact info serializer."""

    class Meta:
        model = ContactInfo
        fields = ['id', 'icon', 'name', 'title', 'info', 'link_url']


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Contact submission serializer for form submissions."""

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

    def create(self, validated_data):
        # Link submission to user account if logged in, enabling reply/follow-up.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class SiteConfigurationSerializer(serializers.ModelSerializer):
    """Site configuration serializer."""

    class Meta:
        model = SiteConfiguration
        # Exclude id since it's always 1 (singleton) and adds no value to API consumers.
        exclude = ['id']
