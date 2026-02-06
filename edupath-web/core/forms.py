"""
Core Forms - Contact form.
"""

from django import forms
from .models import ContactSubmission


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


class ContactForm(forms.ModelForm):
    """
    Contact form for user inquiries.

    Used on the contact page to collect messages from visitors.
    Styled with Tailwind CSS classes.
    """

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Name :'
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Email :'
            }),
            'subject': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Subject :'
            }),
            'message': forms.Textarea(attrs={
                'class': TEXTAREA_CLASSES,
                'placeholder': 'Message :',
                'rows': 4
            }),
        }
