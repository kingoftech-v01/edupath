"""
Core Models - Site configuration, Features, Contact, Statistics, Pricing.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract base model with timestamps.

    Provides automatic timestamp tracking for creation and updates.

    Attributes:
        created_at: When the record was created.
        updated_at: When the record was last modified.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """
    Abstract base model with ordering and soft-delete.

    Provides manual ordering and visibility control.

    Attributes:
        order: Sort order (lower = first).
        is_active: Whether item is visible.
    """
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


# =============================================================================
# FEATURE MODEL
# =============================================================================

class Feature(TimestampedModel, OrderedModel):
    """
    Platform features displayed on homepage.

    Represents key selling points with icons (e.g., "Expert Instructors").

    Attributes:
        icon: CSS icon class.
        title: Feature title.
        desc: Feature description.
        link_url: Optional link for "Learn more".
    """
    icon = models.CharField(
        max_length=100,
        help_text="Icon class (e.g., iconoir-thumbs-up text-3xl)"
    )
    title = models.CharField(max_length=255)
    desc = models.TextField()
    link_url = models.URLField(blank=True)

    def __str__(self):
        """Return feature title as string representation."""
        return self.title


# =============================================================================
# BUSINESS PARTNER MODEL
# =============================================================================

class BusinessPartner(TimestampedModel, OrderedModel):
    """
    Business partner logos.

    Displays partner/client logos in the homepage carousel.

    Attributes:
        name: Partner company name.
        img: Path to logo image.
        website_url: Optional partner website link.
    """
    name = models.CharField(max_length=100)
    img = models.CharField(
        max_length=255,
        help_text="Path to logo image (e.g., /static/assets/images/client/amazon.svg)"
    )
    website_url = models.URLField(blank=True)

    def __str__(self):
        """Return partner name as string representation."""
        return self.name


# =============================================================================
# SITE STATISTIC MODEL
# =============================================================================

class SiteStatistic(TimestampedModel, OrderedModel):
    """
    CTA statistics for animated counters.

    Displays impressive numbers (Courses count, Countries, Students).
    JavaScript animates from 'number' to 'target' on scroll.

    Attributes:
        title: Statistic label.
        number: Starting number for animation.
        target: Target number (what counter animates to).
        symbol: Suffix (e.g., '+', 'K', '%').
    """
    title = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0, help_text="Starting number for animation")
    target = models.PositiveIntegerField(default=0, help_text="Target number for counter")
    symbol = models.CharField(max_length=10, default='+', help_text="Symbol after number")

    class Meta:
        verbose_name = "Site Statistic"
        verbose_name_plural = "Site Statistics"
        ordering = ['order']

    def __str__(self):
        """Return statistic title and value as string representation."""
        return f"{self.title}: {self.target}{self.symbol}"


# =============================================================================
# PRICING PLAN MODEL
# =============================================================================

class PricingPlan(TimestampedModel, OrderedModel):
    """
    Subscription pricing plans.

    Displays pricing cards on the pricing page with features list.

    Attributes:
        name: Plan name (e.g., "Basic", "Pro", "Enterprise").
        price: Plan price.
        duration: Billing period (Week, Month, Year).
        button_text: CTA button text.
        style: CSS classes for plan container.
        button_style: CSS classes for CTA button.
        features: JSON list of included features.
    """
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
        """Return plan name and price as string representation."""
        return f"{self.name} - ${self.price}/{self.duration}"


# =============================================================================
# CONTACT INFO MODEL
# =============================================================================

class ContactInfo(TimestampedModel, OrderedModel):
    """
    Contact information entries.

    Displays contact methods on the contact page (phone, email, location).

    Attributes:
        icon: CSS icon class.
        name: Contact type (e.g., "Phone", "Email").
        title: Description text.
        info: Contact value (phone number, email address).
        link_url: Optional clickable link (mailto:, tel:).
    """
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
        """Return contact type name as string representation."""
        return self.name


# =============================================================================
# CONTACT SUBMISSION MODEL
# =============================================================================

class ContactSubmission(TimestampedModel):
    """
    Contact form submissions.

    Stores messages from the contact form for admin review.

    Attributes:
        name: Sender's name.
        email: Sender's email address.
        subject: Message subject.
        message: Message content.
        status: Processing status (new, read, replied, archived).
        user: Optional link to logged-in user.
    """
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
        """Return sender name and subject as string representation."""
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
        """
        Save configuration, enforcing singleton pattern.

        Forces pk=1 to ensure only one instance exists.

        Args:
            *args: Positional arguments passed to parent save.
            **kwargs: Keyword arguments passed to parent save.
        """
        # Force pk=1 to enforce singleton - any save overwrites the single instance.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """
        Get the singleton configuration instance.

        Creates with defaults if none exists.

        Returns:
            SiteConfiguration: The single configuration instance.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        """Return site name as string representation."""
        return self.site_name
