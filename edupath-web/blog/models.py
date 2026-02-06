"""
Blog Models - Blog posts and articles.
"""

from django.db import models
from django.utils.text import slugify
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


class Blog(TimestampedModel, OrderedModel):
    """
    Blog post model.

    Stores blog articles with optional author relationship.
    Uses 'name' field as a category label (e.g., "Development", "Design").

    Attributes:
        title: Post title.
        slug: URL-friendly identifier (auto-generated).
        name: Category/tag name for grouping.
        content: Full post content (HTML or markdown).
        excerpt: Short preview text (max 500 chars).
        img: Featured image.
        read_time_minutes: Estimated reading time.
        publish_date: When to publish the post.
        author: Foreign key to Instructor model.
    """
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
        """Return blog title as string representation."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Save blog with auto-generated slug.

        Generates URL-friendly slug from title if not provided.

        Args:
            *args: Positional arguments passed to parent save.
            **kwargs: Keyword arguments passed to parent save.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
