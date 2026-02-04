"""
EduPath Admin Configuration - Django admin panel setup.

Registers all models with customized admin interfaces including:
- List displays, filters, and search
- Inline editing for related models
- Custom actions for bulk operations
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Instructor, Course, Blog, Review, Feature,
    BusinessPartner, SiteStatistic, PricingPlan, ContactInfo,
    ContactSubmission, SiteConfiguration
)


# ============================================================================
# INLINE ADMINS
# ============================================================================

class ReviewInline(admin.TabularInline):
    """Inline reviews for Course admin."""
    model = Review
    extra = 0
    fields = ['name', 'rating', 'desc', 'is_active']
    readonly_fields = ['name']


class CourseInline(admin.TabularInline):
    """Inline courses for Category and Instructor admin."""
    model = Course
    extra = 0
    fields = ['title', 'price', 'is_active', 'is_featured']
    readonly_fields = ['title']
    show_change_link = True


class BlogInline(admin.TabularInline):
    """Inline blogs for Instructor admin."""
    model = Blog
    extra = 0
    fields = ['title', 'name', 'is_active']
    readonly_fields = ['title']
    show_change_link = True


# ============================================================================
# CATEGORY ADMIN
# ============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview', 'course_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']
    inlines = [CourseInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'icon', 'description')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def icon_preview(self, obj):
        return format_html('<i class="{}"></i> <code>{}</code>', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'


# ============================================================================
# INSTRUCTOR ADMIN
# ============================================================================

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'title', 'user', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'title', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'title']
    raw_id_fields = ['user']
    inlines = [CourseInline, BlogInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'title', 'bio', 'img', 'user')
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def image_preview(self, obj):
        if obj.img:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'


# ============================================================================
# COURSE ADMIN
# ============================================================================

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


# ============================================================================
# BLOG ADMIN
# ============================================================================

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
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
        if obj.img:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.img.url
            )
        return "-"
    image_preview.short_description = 'Image'


# ============================================================================
# REVIEW ADMIN
# ============================================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'title', 'rating_display', 'course', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['rating', 'is_active', 'course']
    search_fields = ['name', 'desc']
    raw_id_fields = ['user', 'course']

    fieldsets = (
        ('Reviewer Info', {
            'fields': ('name', 'title', 'img', 'user')
        }),
        ('Review', {
            'fields': ('rating', 'desc', 'course')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

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


# ============================================================================
# FEATURE ADMIN
# ============================================================================

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'desc']
    list_filter = ['is_active']

    fieldsets = (
        (None, {
            'fields': ('icon', 'title', 'desc', 'link_url')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def icon_preview(self, obj):
        return format_html('<i class="{}"></i> <code>{}</code>', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'


# ============================================================================
# BUSINESS PARTNER ADMIN
# ============================================================================

@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'img', 'website_url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']

    fieldsets = (
        (None, {
            'fields': ('name', 'img', 'website_url')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


# ============================================================================
# SITE STATISTIC ADMIN
# ============================================================================

@admin.register(SiteStatistic)
class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ['title', 'number', 'target', 'symbol', 'order', 'is_active']
    list_editable = ['number', 'target', 'symbol', 'order', 'is_active']
    list_filter = ['is_active']

    fieldsets = (
        (None, {
            'fields': ('title', 'number', 'target', 'symbol')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


# ============================================================================
# PRICING PLAN ADMIN
# ============================================================================

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'button_text', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    fieldsets = (
        ('Plan Info', {
            'fields': ('name', 'price', 'duration', 'button_text')
        }),
        ('Styling', {
            'fields': ('style', 'button_style'),
            'classes': ('collapse',)
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


# ============================================================================
# CONTACT INFO ADMIN
# ============================================================================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview', 'info', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    fieldsets = (
        (None, {
            'fields': ('icon', 'name', 'title', 'info', 'link_url')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def icon_preview(self, obj):
        return format_html('<i class="{}"></i>', obj.icon)
    icon_preview.short_description = 'Icon'


# ============================================================================
# CONTACT SUBMISSION ADMIN
# ============================================================================

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'user', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Sender Info', {
            'fields': ('name', 'email', 'user')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} submission(s) marked as read.')
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} submission(s) marked as replied.')
    mark_as_replied.short_description = "Mark selected as replied"

    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} submission(s) archived.')
    mark_as_archived.short_description = "Archive selected"

    def has_add_permission(self, request):
        # Submissions are created via form, not admin
        return False


# ============================================================================
# SITE CONFIGURATION ADMIN (Singleton)
# ============================================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Legal', {
            'fields': ('copyright_text',)
        }),
    )

    def has_add_permission(self, request):
        # Only one instance allowed (singleton)
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of site config
        return False


# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

admin.site.site_header = "EduPath Administration"
admin.site.site_title = "EduPath Admin"
admin.site.index_title = "Welcome to EduPath Admin Panel"
