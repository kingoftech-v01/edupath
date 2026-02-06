"""
Core Admin - Site configuration, Features, Contact administration.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Feature, BusinessPartner, SiteStatistic, PricingPlan,
    ContactInfo, ContactSubmission, SiteConfiguration
)


# =============================================================================
# FEATURE ADMIN
# =============================================================================

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """
    Admin for Feature model.

    Features icon preview in list view.
    """
    list_display = ['title', 'icon_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'desc']
    list_filter = ['is_active']

    def icon_preview(self, obj):
        """
        Render icon with its class name in list view.

        Args:
            obj: Feature instance.

        Returns:
            str: HTML with icon and class name.
        """
        return format_html('<i class="{}"></i> <code>{}</code>', obj.icon, obj.icon)
    icon_preview.short_description = 'Icon'


# =============================================================================
# BUSINESS PARTNER ADMIN
# =============================================================================

@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    """
    Admin for BusinessPartner model.

    Manages partner/client logos for homepage carousel.
    """
    list_display = ['name', 'img', 'website_url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']


# =============================================================================
# SITE STATISTIC ADMIN
# =============================================================================

@admin.register(SiteStatistic)
class SiteStatisticAdmin(admin.ModelAdmin):
    """
    Admin for SiteStatistic model.

    Manages CTA counter statistics (students, courses, etc.).
    """
    list_display = ['title', 'number', 'target', 'symbol', 'order', 'is_active']
    list_editable = ['number', 'target', 'symbol', 'order', 'is_active']
    list_filter = ['is_active']


# =============================================================================
# PRICING PLAN ADMIN
# =============================================================================

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    """
    Admin for PricingPlan model.

    Features fieldsets for organizing plan details and styling.
    """
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


# =============================================================================
# CONTACT INFO ADMIN
# =============================================================================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Admin for ContactInfo model.

    Manages contact methods (phone, email, location).
    """
    list_display = ['name', 'icon_preview', 'info', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']

    def icon_preview(self, obj):
        """
        Render icon in list view.

        Args:
            obj: ContactInfo instance.

        Returns:
            str: HTML icon element.
        """
        return format_html('<i class="{}"></i>', obj.icon)
    icon_preview.short_description = 'Icon'


# =============================================================================
# CONTACT SUBMISSION ADMIN
# =============================================================================

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """
    Admin for ContactSubmission model.

    Features bulk actions for status management.
    Submissions are read-only (created via form).
    """
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'user', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']

    def mark_as_read(self, request, queryset):
        """
        Bulk action to mark submissions as read.

        Args:
            request: Admin request.
            queryset: Selected submissions.
        """
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} submission(s) marked as read.')
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_replied(self, request, queryset):
        """
        Bulk action to mark submissions as replied.

        Args:
            request: Admin request.
            queryset: Selected submissions.
        """
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} submission(s) marked as replied.')
    mark_as_replied.short_description = "Mark selected as replied"

    def mark_as_archived(self, request, queryset):
        """
        Bulk action to archive submissions.

        Args:
            request: Admin request.
            queryset: Selected submissions.
        """
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} submission(s) archived.')
    mark_as_archived.short_description = "Archive selected"

    def has_add_permission(self, request):
        """
        Disable manual creation.

        Submissions should only come from the contact form.
        """
        return False


# =============================================================================
# SITE CONFIGURATION ADMIN (Singleton)
# =============================================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """
    Admin for SiteConfiguration singleton.

    Only one instance can exist. Add/delete permissions restricted.
    """
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
        """
        Only allow adding if no configuration exists.

        Enforces singleton pattern.
        """
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of site configuration.

        Configuration should always exist.
        """
        return False


# =============================================================================
# ADMIN SITE CUSTOMIZATION
# =============================================================================

admin.site.site_header = "EduPath Administration"
admin.site.site_title = "EduPath Admin"
admin.site.index_title = "Welcome to EduPath Admin Panel"
