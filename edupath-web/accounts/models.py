"""
Accounts Models - User profiles and authentication.

Uses django-allauth for authentication.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile information."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Profile info
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True, max_length=500)
    phone = models.CharField(max_length=20, blank=True)

    # Social links
    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def full_name(self):
        """Get user's full name or username."""
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        return name or self.user.username


# Signal to create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """Save UserProfile when User is saved (skip on creation to avoid duplicate save)."""
    if not created and hasattr(instance, 'profile'):
        instance.profile.save()
