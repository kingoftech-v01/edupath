"""
Blog Admin - Blog post administration.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Admin for Blog model.

    Features image preview, fieldsets, and date hierarchy.
    """
    list_display = ['title', 'image_preview', 'name', 'author', 'publish_date', 'is_active']
    list_editable = ['is_active']
    list_filter = ['name', 'author', 'is_active', 'publish_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish_date'

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'name', 'author')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Media', {
            'fields': ('img',)
        }),
        ('Metadata', {
            'fields': ('read_time_minutes',)
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def image_preview(self, obj):
        """
        Render blog image thumbnail in list view.

        Args:
            obj: Blog instance.

        Returns:
            str: HTML img tag or "-" if no image.
        """
        if obj.img:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'
