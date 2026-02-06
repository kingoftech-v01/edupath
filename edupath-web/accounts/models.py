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


# Two separate signals handle profile lifecycle: one for creation, one for cascading saves.
# This separation ensures profiles are created atomically with users while still allowing
# profile updates to cascade when User model fields change (e.g., updating first_name).

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    # hasattr check prevents AttributeError during the brief moment between User creation
    # and profile creation (the create_user_profile signal runs first, but Django's signal
    # ordering isn't guaranteed across different signal handlers).
    if hasattr(instance, 'profile'):
        instance.profile.save()
