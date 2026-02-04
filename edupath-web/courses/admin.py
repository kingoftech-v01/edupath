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
    model = Course
    extra = 0
    fields = ['title', 'price', 'is_active', 'is_featured']
    readonly_fields = ['title']
    show_change_link = True


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ['name', 'rating', 'desc', 'is_active']
    readonly_fields = ['name']


# =============================================================================
# CATEGORY ADMIN
# =============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview', 'course_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']
    inlines = [CourseInline]

    def icon_preview(self, obj):
        return format_html('<i class="{}"></i> <code>{}</code>', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'


# =============================================================================
# INSTRUCTOR ADMIN
# =============================================================================

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'title', 'user', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'title', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'title']
    raw_id_fields = ['user']
    inlines = [CourseInline]

    def image_preview(self, obj):
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
    list_display = ['name', 'image_preview', 'title', 'rating_display', 'course', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['rating', 'is_active', 'course']
    search_fields = ['name', 'desc']
    raw_id_fields = ['user', 'course']

    def rating_display(self, obj):
        stars = '<span style="color: gold; font-size: 16px;">' + ('&#9733;' * obj.rating) + ('&#9734;' * (5 - obj.rating)) + '</span>'
        return format_html(stars)
    rating_display.short_description = 'Rating'

    def image_preview(self, obj):
        if obj.img:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'
