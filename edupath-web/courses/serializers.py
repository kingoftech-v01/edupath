"""
Courses Serializers - API serializers for courses app.
"""

from rest_framework import serializers
from .models import Category, Instructor, Course, Review


# =============================================================================
# CATEGORY SERIALIZERS
# =============================================================================

class CategoryListSerializer(serializers.ModelSerializer):
    """Category serializer for listings."""
    course_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

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

    class Meta:
        model = Instructor
        fields = [
            'id', 'name', 'slug', 'title', 'bio', 'img',
            'facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url',
            'course_count', 'created_at'
        ]

    def get_course_count(self, obj):
        return obj.courses.filter(is_active=True).count()


# =============================================================================
# COURSE SERIALIZERS
# =============================================================================

class CourseListSerializer(serializers.ModelSerializer):
    """Course serializer for listings."""
    category = CategoryListSerializer(read_only=True)
    instructor = InstructorListSerializer(read_only=True)
    formatted_price = serializers.CharField(read_only=True)
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

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            course = attrs.get('course')
            if course and Review.objects.filter(user=request.user, course=course).exists():
                raise serializers.ValidationError(
                    'You have already submitted a review for this course.'
                )
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['name'] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)
