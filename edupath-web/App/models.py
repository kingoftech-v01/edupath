"""
EduPath Models - Database models for the learning platform.

This module defines all database models including:
- Category, Instructor, Course, Blog (core content)
- Review, Feature, BusinessPartner (supporting content)
- SiteStatistic, PricingPlan, ContactInfo (site configuration)
- ContactSubmission (user interactions)
- SiteConfiguration (global settings - singleton)
"""

from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone

from courses.models import validate_video_file, _generate_unique_slug


# ============================================================================
# ABSTRACT BASE MODELS
# ============================================================================

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


# ============================================================================
# CATEGORY MODEL
# ============================================================================

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
            self.slug = _generate_unique_slug(Category, self.name, self)
        super().save(*args, **kwargs)

    @property
    def course_count(self):
        return self.courses.filter(is_active=True).count()

    @property
    def title(self):
        """For template compatibility - returns course count display."""
        count = self.course_count
        return f"{count}+ Courses" if count > 0 else "10+ Courses"


# ============================================================================
# INSTRUCTOR MODEL
# ============================================================================

class Instructor(TimestampedModel, OrderedModel):
    """Instructor profiles."""
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='app_instructor_profile'
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
            self.slug = _generate_unique_slug(Instructor, self.name, self)
        super().save(*args, **kwargs)


# ============================================================================
# COURSE MODEL (Enhanced)
# ============================================================================

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
    img1 = models.ImageField(upload_to='course_instructors/', blank=True, help_text="Instructor image for course card")
    video_url = models.URLField(blank=True, help_text="YouTube embed URL")
    video_file = models.FileField(
        upload_to='course_videos/', blank=True, validators=[validate_video_file]
    )

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
            self.slug = _generate_unique_slug(Course, self.title, self)
        self.is_free = self.price <= Decimal('0')
        # Auto-fill name from instructor if not set
        if not self.name and self.instructor:
            self.name = self.instructor.name
        super().save(*args, **kwargs)

    @property
    def formatted_price(self):
        """Return formatted price string."""
        if self.is_free or self.price == 0:
            return "$0"
        return f"${self.price:.0f}"

    # Aliases for template compatibility with context_processors data format
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


# ============================================================================
# BLOG MODEL (Enhanced)
# ============================================================================

class Blog(TimestampedModel, OrderedModel):
    """Blog post model."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=100, help_text="Category name (e.g., Degree, University, Developer)")
    content = models.TextField(blank=True)
    excerpt = models.TextField(blank=True, max_length=500)

    # Media
    img = models.ImageField(upload_to='blog_images/')

    # Metadata
    read_time_minutes = models.PositiveIntegerField(default=5)
    publish_date = models.DateField(default=timezone.now)

    # Relationships
    author = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='app_blogs'
    )

    class Meta:
        ordering = ['-publish_date', 'order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(Blog, self.title, self)
        super().save(*args, **kwargs)


# ============================================================================
# REVIEW MODEL
# ============================================================================

class Review(TimestampedModel, OrderedModel):
    """Student reviews/testimonials."""
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100, default="Student")
    img = models.ImageField(upload_to='reviews/', blank=True)
    desc = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])

    # Optional relationships
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='app_reviews')
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


# ============================================================================
# FEATURE MODEL
# ============================================================================

class Feature(TimestampedModel, OrderedModel):
    """Platform features displayed on homepage."""
    icon = models.CharField(
        max_length=100,
        help_text="Icon class (e.g., iconoir-thumbs-up text-3xl)"
    )
    title = models.CharField(max_length=255)
    desc = models.TextField()
    link_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


# ============================================================================
# BUSINESS PARTNER MODEL
# ============================================================================

class BusinessPartner(TimestampedModel, OrderedModel):
    """Business partner logos."""
    name = models.CharField(max_length=100)
    img = models.CharField(
        max_length=255,
        help_text="Path to logo image (e.g., /static/assets/images/client/amazon.svg)"
    )
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


# ============================================================================
# SITE STATISTIC MODEL
# ============================================================================

class SiteStatistic(TimestampedModel, OrderedModel):
    """CTA statistics (Courses count, Countries, Students, Instructors)."""
    title = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0, help_text="Starting number for animation")
    target = models.PositiveIntegerField(default=0, help_text="Target number for counter")
    symbol = models.CharField(max_length=10, default='+', help_text="Symbol after number (e.g., +, K)")

    class Meta:
        verbose_name = "Site Statistic"
        verbose_name_plural = "Site Statistics"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.target}{self.symbol}"


# ============================================================================
# PRICING PLAN MODEL
# ============================================================================

class PricingPlan(TimestampedModel, OrderedModel):
    """Subscription pricing plans."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50, help_text="e.g., Week, Month, Year")
    button_text = models.CharField(max_length=50, default="Join Now")

    # Styling (preserves template styling)
    style = models.TextField(
        blank=True,
        help_text="CSS classes for the plan container",
        default="group md:flex items-center justify-between p-6 rounded-lg shadow hover:shadow-md shadow-slate-100 dark:shadow-slate-800 transition-all duration-500"
    )
    button_style = models.TextField(
        blank=True,
        help_text="CSS classes for button",
        default="h-8 px-3 tracking-wide inline-flex items-center justify-center font-medium rounded-md bg-violet-600 text-white text-sm md:mt-0 mt-4"
    )

    # Features list
    features = models.JSONField(default=list, blank=True, help_text="List of plan features")

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.duration}"


# ============================================================================
# CONTACT INFO MODEL
# ============================================================================

class ContactInfo(TimestampedModel, OrderedModel):
    """Contact information entries."""
    icon = models.CharField(max_length=100, help_text="Icon class (e.g., iconoir-phone text-3xl)")
    name = models.CharField(max_length=100, help_text="e.g., Phone, Email, Location")
    title = models.TextField(help_text="Description text")
    info = models.CharField(max_length=255, help_text="Contact value (phone, email, address)")
    link_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"
        ordering = ['order']

    def __str__(self):
        return self.name


# ============================================================================
# CONTACT SUBMISSION MODEL
# ============================================================================

class ContactSubmission(TimestampedModel):
    """Contact form submissions."""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    # Status tracking
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Optional: link to user if logged in
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='app_contact_submissions')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ============================================================================
# SITE CONFIGURATION MODEL (Singleton)
# ============================================================================

class SiteConfiguration(models.Model):
    """Site-wide configuration (singleton pattern)."""
    site_name = models.CharField(max_length=255, default="EduPath")
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)

    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    # Social Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # SEO
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)

    # Copyright
    copyright_text = models.CharField(max_length=255, blank=True, default="2024")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name
