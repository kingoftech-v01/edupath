"""
Courses Serializers - API serializers for courses app.
"""

from rest_framework import serializers
from .models import Category, Instructor, Course, Review


# =============================================================================
# CATEGORY SERIALIZERS
# =============================================================================

class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category serializer for listings.

    Includes course count and formatted title for UI display.
    """
    course_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'course_count', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Category serializer with full details.

    Includes description and timestamp for detail views.
    """
    course_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'course_count', 'created_at']


# =============================================================================
# INSTRUCTOR SERIALIZERS
# =============================================================================

class InstructorListSerializer(serializers.ModelSerializer):
    """
    Instructor serializer for listings.

    Minimal fields for card/grid displays.
    """

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'slug', 'title', 'img']


class InstructorDetailSerializer(serializers.ModelSerializer):
    """
    Instructor serializer with full details.

    Includes bio, social links, and course count for profile pages.
    """
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = [
            'id', 'name', 'slug', 'title', 'bio', 'img',
            'facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url',
            'course_count', 'created_at'
        ]

    def get_course_count(self, obj):
        """
        Count active courses by this instructor.

        Args:
            obj: Instructor instance.

        Returns:
            int: Number of active courses.
        """
        return obj.courses.filter(is_active=True).count()


# =============================================================================
# COURSE SERIALIZERS
# =============================================================================

class CourseListSerializer(serializers.ModelSerializer):
    """
    Course serializer for listings.

    Includes nested category/instructor and formatted fields for cards.
    """
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
        """
        Get video file URL if exists.

        Args:
            obj: Course instance.

        Returns:
            str: Video file URL or empty string.
        """
        if obj.video_file:
            return obj.video_file.url
        return ""


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Course serializer with full details.

    Includes full nested objects and recent reviews for detail pages.
    """
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
        """
        Get recent reviews for this course.

        Limited to 5 for performance. Full list via reviews API.

        Args:
            obj: Course instance.

        Returns:
            list: Serialized review data.
        """
        # Limit to 5 reviews for performance; full list available via reviews API.
        # is_active=True excludes soft-deleted or moderated reviews.
        reviews = obj.reviews.filter(is_active=True)[:5]
        return ReviewSerializer(reviews, many=True).data


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Course serializer for create/update operations.

    Admin-only. Allows setting relationships and all editable fields.
    """

    class Meta:
        model = Course
        fields = [
            'title', 'name', 'desc', 'img', 'img1', 'video_url', 'video_file',
            'price', 'lessons', 'students', 'duration_hours',
            'category', 'instructor', 'is_featured', 'is_event', 'is_active', 'order'
        ]
        extra_kwargs = {
            'img': {'required': False},
        }


# =============================================================================
# REVIEW SERIALIZERS
# =============================================================================

class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer for display.

    Read-only serializer for showing reviews in UI.
    """

    class Meta:
        model = Review
        fields = ['id', 'name', 'title', 'img', 'desc', 'rating', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Review serializer for creation.

    Auto-populates user and name from request context.
    """

    class Meta:
        model = Review
        fields = ['course', 'desc', 'rating']

    def create(self, validated_data):
        """
        Create review with auto-populated user data.

        Sets user and name from request context to prevent spoofing.

        Args:
            validated_data: Validated form data.

        Returns:
            Review: Created review instance.
        """
        # Auto-populate user and name from authenticated request to prevent spoofing.
        # Users can't claim to be someone else when leaving reviews.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['name'] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)
