"""
Blog Models - Blog posts and articles.
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from courses.models import _generate_unique_slug


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


class Blog(TimestampedModel, OrderedModel):
    """Blog post model."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=100, help_text="Category name (e.g., Degree, Developer)")
    content = models.TextField(blank=True)
    excerpt = models.TextField(blank=True, max_length=500)

    # Media
    img = models.ImageField(upload_to='blog_images/')

    # Metadata
    read_time_minutes = models.PositiveIntegerField(default=5)
    publish_date = models.DateField(default=timezone.now)

    # Relationships
    author = models.ForeignKey(
        'courses.Instructor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blogs'
    )

    class Meta:
        ordering = ['-publish_date', 'order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(Blog, self.title, self)
        super().save(*args, **kwargs)
