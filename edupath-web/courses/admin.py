"""
Courses Admin - Course, Category, Instructor administration.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Instructor, Course, Review


# =============================================================================
# INLINES
# =============================================================================

class CourseInline(admin.TabularInline):
    """
    Inline for displaying courses in Category/Instructor admin.

    Shows minimal course info with link to full course admin.
    """
    model = Course
    extra = 0
    fields = ['title', 'price', 'is_active', 'is_featured']
    readonly_fields = ['title']
    show_change_link = True


class ReviewInline(admin.TabularInline):
    """
    Inline for displaying reviews in Course admin.

    Allows quick moderation of course reviews.
    """
    model = Review
    extra = 0
    fields = ['name', 'rating', 'desc', 'is_active']
    readonly_fields = ['name']


# =============================================================================
# CATEGORY ADMIN
# =============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category model.

    Features icon preview and inline course listing.
    """
    list_display = ['name', 'icon_preview', 'course_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']
    inlines = [CourseInline]

    def icon_preview(self, obj):
        """
        Render icon with its class name in list view.

        Args:
            obj: Category instance.

        Returns:
            str: HTML with icon and class name.
        """
        return format_html('<i class="{}"></i> <code>{}</code>', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'


# =============================================================================
# INSTRUCTOR ADMIN
# =============================================================================

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """
    Admin for Instructor model.

    Features image preview and inline course listing.
    """
    list_display = ['name', 'image_preview', 'title', 'user', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'title', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'title']
    raw_id_fields = ['user']
    inlines = [CourseInline]

    def image_preview(self, obj):
        """
        Render circular image thumbnail in list view.

        Args:
            obj: Instructor instance.

        Returns:
            str: HTML img tag or "-" if no image.
        """
        if obj.img:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'


# =============================================================================
# COURSE ADMIN
# =============================================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin for Course model.

    Features image preview, fieldsets, and inline reviews.
    """
    list_display = [
        'title', 'image_preview', 'category', 'instructor',
        'formatted_price', 'students', 'is_featured', 'is_active'
    ]
    list_editable = ['is_featured', 'is_active']
    list_filter = ['category', 'instructor', 'is_featured', 'is_free', 'is_active']
    search_fields = ['title', 'desc', 'name']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['category', 'instructor']
    inlines = [ReviewInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'name', 'desc')
        }),
        ('Relationships', {
            'fields': ('category', 'instructor')
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Media', {
            'fields': ('img', 'img1', 'video_url', 'video_file')
        }),
        ('Statistics', {
            'fields': ('lessons', 'students', 'duration_hours')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_event', 'is_active', 'order')
        }),
    )

    def image_preview(self, obj):
        """
        Render course thumbnail in list view.

        Args:
            obj: Course instance.

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


# =============================================================================
# REVIEW ADMIN
# =============================================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin for Review model.

    Features star rating display and image preview.
    """
    list_display = ['name', 'image_preview', 'title', 'rating_display', 'course', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['rating', 'is_active', 'course']
    search_fields = ['name', 'desc']
    raw_id_fields = ['user', 'course']

    def rating_display(self, obj):
        """
        Render star rating as HTML.

        Args:
            obj: Review instance.

        Returns:
            str: HTML with filled/empty star symbols.
        """
        stars = '<span style="color: gold; font-size: 16px;">' + ('&#9733;' * obj.rating) + ('&#9734;' * (5 - obj.rating)) + '</span>'
        return format_html(stars)
    rating_display.short_description = 'Rating'

    def image_preview(self, obj):
        """
        Render reviewer avatar in list view.

        Args:
            obj: Review instance.

        Returns:
            str: HTML img tag or "-" if no image.
        """
        if obj.img:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'
