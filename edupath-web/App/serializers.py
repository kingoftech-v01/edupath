"""
EduPath API Serializers - Django REST Framework serializers.

Provides serializers for all models including:
- List serializers (minimal fields for listings)
- Detail serializers (full fields for detail views)
- Create/Update serializers (writable fields)
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Instructor, Course, Blog, Review, Feature,
    BusinessPartner, SiteStatistic, PricingPlan, ContactInfo,
    ContactSubmission, SiteConfiguration
)


# =============================================================================
# USER SERIALIZERS
# =============================================================================

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer."""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id', 'username']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


# =============================================================================
# CATEGORY SERIALIZERS
# =============================================================================

class CategoryListSerializer(serializers.ModelSerializer):
    """Category serializer for listings."""
    course_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)  # Property that returns "X+ Courses"

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'course_count', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Category serializer with full details."""
    course_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'course_count', 'created_at']


# =============================================================================
# INSTRUCTOR SERIALIZERS
# =============================================================================

class InstructorListSerializer(serializers.ModelSerializer):
    """Instructor serializer for listings."""

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'slug', 'title', 'img']


class InstructorDetailSerializer(serializers.ModelSerializer):
    """Instructor serializer with full details."""
    course_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = [
            'id', 'name', 'slug', 'title', 'bio', 'img', 'user',
            'facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url',
            'course_count', 'created_at'
        ]

    def get_course_count(self, obj):
        return obj.courses.filter(is_active=True).count()


# =============================================================================
# COURSE SERIALIZERS
# =============================================================================

class CourseListSerializer(serializers.ModelSerializer):
    """Course serializer for listings - matches context_processors format."""
    category = CategoryListSerializer(read_only=True)
    instructor = InstructorListSerializer(read_only=True)
    formatted_price = serializers.CharField(read_only=True)

    # Template compatibility fields
    img1 = serializers.ImageField(read_only=True)
    video = serializers.URLField(source='video_url', read_only=True)
    src = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'name', 'desc', 'img', 'img1',
            'price', 'formatted_price', 'lessons', 'students',
            'is_free', 'is_featured', 'video', 'src',
            'category', 'instructor'
        ]

    def get_src(self, obj):
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return ""


class CourseDetailSerializer(serializers.ModelSerializer):
    """Course serializer with full details."""
    category = CategoryDetailSerializer(read_only=True)
    instructor = InstructorDetailSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    formatted_price = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'name', 'desc', 'img', 'img1',
            'video_url', 'video_file', 'price', 'formatted_price',
            'is_free', 'lessons', 'students', 'duration_hours',
            'category', 'instructor', 'is_featured', 'is_event',
            'reviews', 'created_at', 'updated_at'
        ]

    def get_reviews(self, obj):
        reviews = obj.reviews.filter(is_active=True)[:5]
        return ReviewSerializer(reviews, many=True).data


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Course serializer for create/update operations."""

    class Meta:
        model = Course
        fields = [
            'title', 'name', 'desc', 'img', 'img1', 'video_url', 'video_file',
            'price', 'lessons', 'students', 'duration_hours',
            'category', 'instructor', 'is_featured', 'is_event', 'is_active', 'order'
        ]


# =============================================================================
# BLOG SERIALIZERS
# =============================================================================

class BlogListSerializer(serializers.ModelSerializer):
    """Blog serializer for listings."""
    author = InstructorListSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'img', 'name',
            'read_time_minutes', 'publish_date', 'author', 'excerpt'
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    """Blog serializer with full details."""
    author = InstructorDetailSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'img',
            'name', 'read_time_minutes', 'publish_date', 'author',
            'created_at', 'updated_at'
        ]


# =============================================================================
# REVIEW SERIALIZERS
# =============================================================================

class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer for display."""

    class Meta:
        model = Review
        fields = ['id', 'name', 'title', 'img', 'desc', 'rating', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Review serializer for creation."""

    class Meta:
        model = Review
        fields = ['course', 'desc', 'rating']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['name'] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)


# =============================================================================
# STATIC CONTENT SERIALIZERS
# =============================================================================

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


# =============================================================================
# CONTACT SUBMISSION SERIALIZERS
# =============================================================================

class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Contact submission serializer for form submissions."""

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


# =============================================================================
# SITE CONFIGURATION SERIALIZER
# =============================================================================

class SiteConfigurationSerializer(serializers.ModelSerializer):
    """Site configuration serializer."""

    class Meta:
        model = SiteConfiguration
        exclude = ['id']


# =============================================================================
# COMBINED/AGGREGATE SERIALIZERS
# =============================================================================

class HomepageDataSerializer(serializers.Serializer):
    """Combined serializer for all homepage data."""
    features = FeatureSerializer(many=True)
    business_partners = BusinessPartnerSerializer(many=True)
    categories = CategoryListSerializer(many=True)
    featured_courses = CourseListSerializer(many=True)
    instructors = InstructorListSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    statistics = SiteStatisticSerializer(many=True)
    recent_blogs = BlogListSerializer(many=True)
