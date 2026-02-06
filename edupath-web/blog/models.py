"""Blog models."""

from django.db import models
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
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order']


class Blog(TimestampedModel, OrderedModel):
    """Blog post with optional author."""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # 'name' acts as category label for grouping (e.g., "Development", "Design")
    name = models.CharField(max_length=100, help_text="Category name (e.g., Degree, Developer)")
    content = models.TextField(blank=True)
    excerpt = models.TextField(blank=True, max_length=500)

    img = models.ImageField(upload_to='blog_images/')

    read_time_minutes = models.PositiveIntegerField(default=5)
    publish_date = models.DateField(default=timezone.now)

    # Author links to Instructor for consistent instructor-led content branding
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
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
