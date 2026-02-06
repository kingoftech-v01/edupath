"""User profiles. Auth handled by django-allauth."""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user data beyond Django's built-in User model."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True, max_length=500)
    phone = models.CharField(max_length=20, blank=True)

    website = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    email_notifications = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def full_name(self):
        """Falls back to username if first/last name not set."""
        name = f"{self.user.first_name} {self.user.last_name}".strip()
        return name or self.user.username


# Separate signals for create vs update: ensures atomic profile creation while
# still cascading User field changes (e.g., first_name) to the profile.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile for new users."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Cascade User saves to profile."""
    # hasattr guards against race between User and profile creation signals
    if hasattr(instance, 'profile'):
        instance.profile.save()
