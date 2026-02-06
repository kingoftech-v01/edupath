"""
Courses Models - Categories, Instructors, Courses, Reviews.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


# =============================================================================
# ABSTRACT BASE MODELS
# =============================================================================

class TimestampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Abstract base model with ordering support."""
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


# =============================================================================
# CATEGORY MODEL
# =============================================================================

class Category(TimestampedModel, OrderedModel):
    """Course categories like Web Development, Data Science, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(
        max_length=100,
        help_text="Icon class (e.g., iconoir-laptop-dev-mode text-2xl)",
        default="iconoir-book text-2xl"
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def course_count(self):
        return self.courses.filter(is_active=True).count()

    @property
    def title(self):
        """For template compatibility."""
        count = self.course_count
        # "10+ Courses" fallback for empty categories maintains visual consistency
        # on the homepage grid where all category cards need similar formatting.
        return f"{count}+ Courses" if count > 0 else "10+ Courses"


# =============================================================================
# INSTRUCTOR MODEL
# =============================================================================

class Instructor(TimestampedModel, OrderedModel):
    """Instructor profiles."""
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instructor_profile'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=255, help_text="e.g., UI/UX Expert, Science Teacher")
    bio = models.TextField(blank=True)
    img = models.ImageField(upload_to='instructors/', blank=True)

    # Social links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# =============================================================================
# COURSE MODEL
# =============================================================================

class Course(TimestampedModel, OrderedModel):
    """Course model with full details and relationships."""
    # Basic fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, blank=True, help_text="Instructor name for display")
    desc = models.TextField()

    # Pricing
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)

    # Media
    img = models.ImageField(upload_to='course_images/')
    img1 = models.ImageField(upload_to='course_instructors/', blank=True)
    video_url = models.URLField(blank=True, help_text="YouTube embed URL")
    video_file = models.FileField(upload_to='course_videos/', blank=True)

    # Statistics
    lessons = models.PositiveIntegerField(default=0)
    students = models.PositiveIntegerField(default=0)
    duration_hours = models.PositiveIntegerField(default=0)

    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    # Flags
    is_featured = models.BooleanField(default=False)
    is_event = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Derive is_free from price on every save to keep them in sync.
        # Using save() rather than a property ensures database queries can filter on is_free.
        self.is_free = self.price == 0
        # Auto-populate instructor display name for templates that expect course.name
        # without needing to traverse the instructor relationship.
        if not self.name and self.instructor:
            self.name = self.instructor.name
        super().save(*args, **kwargs)

    @property
    def formatted_price(self):
        if self.is_free or self.price == 0:
            return "$0"
        return f"${self.price:.0f}"

    @property
    def video(self):
        """Alias for video_url for template compatibility."""
        return self.video_url

    @property
    def src(self):
        """Alias for video_file URL for template compatibility."""
        if self.video_file:
            return self.video_file.url
        return ""


# =============================================================================
# REVIEW MODEL
# =============================================================================

class Review(TimestampedModel, OrderedModel):
    """Student reviews/testimonials."""
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100, default="Student")
    img = models.ImageField(upload_to='reviews/', blank=True)
    desc = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])

    # Optional relationships
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews'
    )

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
