"""Course serializers."""

from rest_framework import serializers
from .models import Category, Instructor, Course, Review


class CategoryListSerializer(serializers.ModelSerializer):
    """Minimal category fields for list views."""
    course_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'course_count', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Full category fields for detail views."""
    course_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'course_count', 'created_at']


class InstructorListSerializer(serializers.ModelSerializer):
    """Minimal instructor fields for cards/grids."""

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'slug', 'title', 'img']


class InstructorDetailSerializer(serializers.ModelSerializer):
    """Full instructor fields for profile pages."""
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


class CourseListSerializer(serializers.ModelSerializer):
    """Course with nested relations for list views."""
    category = CategoryListSerializer(read_only=True)
    instructor = InstructorListSerializer(read_only=True)
    formatted_price = serializers.CharField(read_only=True)
    # Aliases for template compatibility
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
            return obj.video_file.url
        return ""


class CourseDetailSerializer(serializers.ModelSerializer):
    """Full course with reviews for detail pages."""
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
        # Limit 5 for performance; full list via /reviews/?course=X
        reviews = obj.reviews.filter(is_active=True)[:5]
        return ReviewSerializer(reviews, many=True).data


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Admin-only write serializer."""

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


class ReviewSerializer(serializers.ModelSerializer):
    """Read-only review for display."""

    class Meta:
        model = Review
        fields = ['id', 'name', 'title', 'img', 'desc', 'rating', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Write-only review creation."""

    class Meta:
        model = Review
        fields = ['course', 'desc', 'rating']

    def create(self, validated_data):
        # Auto-populate user/name from request to prevent identity spoofing
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['name'] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)
