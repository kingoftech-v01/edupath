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
    """
    Abstract base model with created/updated timestamps.

    Provides automatic timestamp tracking for model creation and updates.
    Inherit from this class to add created_at/updated_at fields.

    Attributes:
        created_at: Timestamp when record was created.
        updated_at: Timestamp of last modification.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """
    Abstract base model with ordering and soft-delete support.

    Provides manual ordering via 'order' field and soft-delete via 'is_active'.
    Lower order values appear first. Inactive items are hidden from public views.

    Attributes:
        order: Sort order (lower = first).
        is_active: Whether item is visible/active.
    """
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


# =============================================================================
# CATEGORY MODEL
# =============================================================================

class Category(TimestampedModel, OrderedModel):
    """
    Course categories like Web Development, Data Science, etc.

    Groups courses into logical categories for browsing and filtering.
    Each category has an icon for visual representation in the UI.

    Attributes:
        name: Unique category name.
        slug: URL-friendly identifier (auto-generated from name).
        icon: CSS icon class for display.
        description: Detailed category description.
    """
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
        """Return category name as string representation."""
        return self.name

    def save(self, *args, **kwargs):
        """
        Save category with auto-generated slug.

        Generates a URL-friendly slug from the name if not provided.

        Args:
            *args: Positional arguments passed to parent save.
            **kwargs: Keyword arguments passed to parent save.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def course_count(self):
        """
        Count of active courses in this category.

        Returns:
            int: Number of active courses.
        """
        return self.courses.filter(is_active=True).count()

    @property
    def title(self):
        """
        Formatted course count string for template display.

        Returns "X+ Courses" or "10+ Courses" fallback for empty categories
        to maintain visual consistency on the homepage category grid.

        Returns:
            str: Formatted course count label.
        """
        count = self.course_count
        # "10+ Courses" fallback for empty categories maintains visual consistency
        # on the homepage grid where all category cards need similar formatting.
        return f"{count}+ Courses" if count > 0 else "10+ Courses"


# =============================================================================
# INSTRUCTOR MODEL
# =============================================================================

class Instructor(TimestampedModel, OrderedModel):
    """
    Instructor profiles.

    Represents course instructors with their bio and social links.
    Can optionally link to a User account for login capabilities.

    Attributes:
        user: Optional link to Django User for authentication.
        name: Display name.
        slug: URL-friendly identifier.
        title: Professional title (e.g., "UI/UX Expert").
        bio: Instructor biography.
        img: Profile image.
        facebook_url: Facebook profile link.
        instagram_url: Instagram profile link.
        linkedin_url: LinkedIn profile link.
        twitter_url: Twitter profile link.
    """
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
        """Return instructor name as string representation."""
        return self.name

    def save(self, *args, **kwargs):
        """
        Save instructor with auto-generated slug.

        Generates a URL-friendly slug from the name if not provided.

        Args:
            *args: Positional arguments passed to parent save.
            **kwargs: Keyword arguments passed to parent save.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# =============================================================================
# COURSE MODEL
# =============================================================================

class Course(TimestampedModel, OrderedModel):
    """
    Course model with full details and relationships.

    The central model for educational content. Supports both YouTube
    embeds (video_url) and self-hosted videos (video_file).

    Attributes:
        title: Course title.
        slug: URL-friendly identifier.
        name: Instructor name for display (auto-populated from instructor).
        desc: Course description.
        price: Course price (0 for free courses).
        is_free: Boolean derived from price on save.
        img: Course thumbnail image.
        img1: Instructor image for course cards.
        video_url: YouTube embed URL.
        video_file: Self-hosted video file.
        lessons: Number of lessons.
        students: Number of enrolled students.
        duration_hours: Total course duration.
        category: Foreign key to Category.
        instructor: Foreign key to Instructor.
        is_featured: Show on homepage featured section.
        is_event: Marks course as event (webinar, workshop).
    """
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
        """Return course title as string representation."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Save course with auto-generated fields.

        Handles:
        - Slug generation from title
        - is_free derivation from price
        - Instructor name population

        Args:
            *args: Positional arguments passed to parent save.
            **kwargs: Keyword arguments passed to parent save.
        """
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
        """
        Format price for display.

        Returns:
            str: "$0" for free courses, otherwise "$XX".
        """
        if self.is_free or self.price == 0:
            return "$0"
        return f"${self.price:.0f}"

    @property
    def video(self):
        """
        Alias for video_url for template compatibility.

        Returns:
            str: YouTube embed URL or empty string.
        """
        return self.video_url

    @property
    def src(self):
        """
        Alias for video_file URL for template compatibility.

        Returns:
            str: Video file URL or empty string if no file.
        """
        if self.video_file:
            return self.video_file.url
        return ""


# =============================================================================
# REVIEW MODEL
# =============================================================================

class Review(TimestampedModel, OrderedModel):
    """
    Student reviews and testimonials.

    Stores course reviews with ratings. Can be standalone testimonials
    or linked to specific courses and users.

    Attributes:
        name: Reviewer name (can be auto-populated from user).
        title: Reviewer title (e.g., "Student", "Graduate").
        img: Reviewer avatar image.
        desc: Review text content.
        rating: Star rating 1-5.
        user: Optional link to User who wrote review.
        course: Optional link to reviewed Course.
    """
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
        """Return reviewer name and rating as string representation."""
        return f"{self.name} - {self.rating} stars"
