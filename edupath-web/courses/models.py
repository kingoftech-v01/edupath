"""Courses app models."""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class TimestampedModel(models.Model):
    """Abstract base with created/updated timestamps."""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Abstract base with manual ordering and soft-delete."""
    order = models.PositiveIntegerField(default=0)
    # Soft-delete: inactive items hidden from public views but preserved for auditing
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


class Category(TimestampedModel, OrderedModel):
    """Course category (e.g., Web Development, Data Science)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    # Icon uses Iconoir CSS classes for the frontend category grid
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
        """Homepage grid display label."""
        count = self.course_count
        # Fallback "10+" for empty categories keeps homepage grid visually consistent
        return f"{count}+ Courses" if count > 0 else "10+ Courses"


class Instructor(TimestampedModel, OrderedModel):
    """Instructor profile with bio and social links."""
    # Optional User link enables instructor login to manage their courses
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


class Course(TimestampedModel, OrderedModel):
    """Course with content, pricing, and instructor."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # Denormalized instructor name for templates that don't need full instructor object
    name = models.CharField(max_length=255, blank=True, help_text="Instructor name for display")
    desc = models.TextField()

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # Derived field enables database-level filtering (is_free=True in queries)
    is_free = models.BooleanField(default=False)

    img = models.ImageField(upload_to='course_images/')
    img1 = models.ImageField(upload_to='course_instructors/', blank=True)
    # Supports both YouTube embeds and self-hosted videos
    video_url = models.URLField(blank=True, help_text="YouTube embed URL")
    video_file = models.FileField(upload_to='course_videos/', blank=True)

    lessons = models.PositiveIntegerField(default=0)
    students = models.PositiveIntegerField(default=0)
    duration_hours = models.PositiveIntegerField(default=0)

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

    is_featured = models.BooleanField(default=False)
    # Events are webinars/workshops with time-based availability
    is_event = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Sync is_free with price for database query filtering
        self.is_free = self.price == 0
        # Denormalize instructor name for templates
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
        """Template alias for video_url."""
        return self.video_url

    @property
    def src(self):
        """Template alias for video_file URL."""
        if self.video_file:
            return self.video_file.url
        return ""


class Review(TimestampedModel, OrderedModel):
    """Student review or testimonial."""
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100, default="Student")
    img = models.ImageField(upload_to='reviews/', blank=True)
    desc = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])

    # Optional links - supports both standalone testimonials and course-specific reviews
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
