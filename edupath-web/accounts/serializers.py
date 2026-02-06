"""
Accounts Serializers - User and profile serializers.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.

    Includes user fields (username, email, names) as read-only nested data.
    Profile fields (bio, phone, social links) are editable.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'avatar', 'bio', 'phone', 'website',
            'linkedin_url', 'twitter_url', 'github_url',
            'email_notifications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with nested profile.

    Read-only serializer that includes the full UserProfile as nested data.
    Used for current user endpoint and authentication responses.
    """
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'profile']
        read_only_fields = ['id', 'username']

    def get_full_name(self, obj):
        """
        Compute user's full name from first and last name.

        Args:
            obj: User instance being serialized.

        Returns:
            str: Full name or username as fallback.
        """
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name or obj.username
