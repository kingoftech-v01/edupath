"""
Accounts Forms - Profile and user forms.
"""

from django import forms
from .models import UserProfile


# Tailwind CSS classes
INPUT_CLASSES = (
    "w-full py-2 px-3 border border-slate-100 dark:border-slate-800 "
    "focus:border-violet-600/30 dark:focus:border-violet-600/30 "
    "bg-transparent focus:outline-none rounded-md h-10 mt-3"
)

TEXTAREA_CLASSES = (
    "w-full py-2 px-3 border border-slate-100 dark:border-slate-800 "
    "focus:border-violet-600/30 dark:focus:border-violet-600/30 "
    "bg-transparent focus:ring-0 focus:outline-none rounded-md h-28 mt-2"
)


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile.

    Includes User model fields (first_name, last_name) alongside
    UserProfile fields. The view handles saving to both models.
    Styled with Tailwind CSS classes for consistent UI.
    """
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Last Name'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'phone', 'website', 'linkedin_url', 'twitter_url', 'github_url', 'email_notifications']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': TEXTAREA_CLASSES,
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Phone Number'
            }),
            'website': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Website URL'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'LinkedIn URL'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Twitter URL'
            }),
            'github_url': forms.URLInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'GitHub URL'
            }),
        }
