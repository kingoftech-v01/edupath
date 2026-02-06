"""
Core Models - Site configuration, Features, Contact, Statistics, Pricing.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimestampedModel(models.Model):
    """Abstract base model with timestamps."""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Abstract base model with ordering."""
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


# =============================================================================
# FEATURE MODEL
# =============================================================================

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


# =============================================================================
# BUSINESS PARTNER MODEL
# =============================================================================

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


# =============================================================================
# SITE STATISTIC MODEL
# =============================================================================

class SiteStatistic(TimestampedModel, OrderedModel):
    """CTA statistics (Courses count, Countries, Students, Instructors)."""
    title = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0, help_text="Starting number for animation")
    target = models.PositiveIntegerField(default=0, help_text="Target number for counter")
    symbol = models.CharField(max_length=10, default='+', help_text="Symbol after number")

    class Meta:
        verbose_name = "Site Statistic"
        verbose_name_plural = "Site Statistics"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.target}{self.symbol}"


# =============================================================================
# PRICING PLAN MODEL
# =============================================================================

class PricingPlan(TimestampedModel, OrderedModel):
    """Subscription pricing plans."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50, help_text="e.g., Week, Month, Year")
    button_text = models.CharField(max_length=50, default="Join Now")

    # Styling
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


# =============================================================================
# CONTACT INFO MODEL
# =============================================================================

class ContactInfo(TimestampedModel, OrderedModel):
    """Contact information entries."""
    icon = models.CharField(max_length=100, help_text="Icon class")
    name = models.CharField(max_length=100, help_text="e.g., Phone, Email, Location")
    title = models.TextField(help_text="Description text")
    info = models.CharField(max_length=255, help_text="Contact value")
    link_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"
        ordering = ['order']

    def __str__(self):
        return self.name


# =============================================================================
# CONTACT SUBMISSION MODEL
# =============================================================================

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

    # Optional user link
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.subject}"


# =============================================================================
# SITE CONFIGURATION MODEL (Singleton)
# =============================================================================

class SiteConfiguration(models.Model):
    """
    Site-wide configuration using a singleton pattern.

    Only one instance (pk=1) can exist. Use SiteConfiguration.get_solo() to retrieve it.
    This simplifies admin UI and avoids accidental multiple configs.
    """
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
        # Force pk=1 to enforce singleton - any save overwrites the single instance.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Always use this to get config; creates with defaults if none exists."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name
