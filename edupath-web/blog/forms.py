"""
Blog Forms - Search and filtering forms for blog posts.
"""

from django import forms


# Tailwind CSS classes for form styling
INPUT_CLASSES = (
    "w-full py-2 px-3 border border-slate-100 dark:border-slate-800 "
    "focus:border-violet-600/30 dark:focus:border-violet-600/30 "
    "bg-transparent focus:outline-none rounded-md h-10"
)

SELECT_CLASSES = (
    "w-full py-2 px-3 border border-slate-100 dark:border-slate-800 "
    "focus:border-violet-600/30 dark:focus:border-violet-600/30 "
    "bg-transparent focus:outline-none rounded-md h-10"
)


class BlogSearchForm(forms.Form):
    """Search and filter form for blog listing."""

    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Search blogs...',
        })
    )

    category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': SELECT_CLASSES,
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate category choices from existing blog categories
        self.fields['category'].choices = self._get_category_choices()

    def _get_category_choices(self):
        """Get unique category names from blogs."""
        from .models import Blog
        # Blog uses `name` field as freeform category (e.g., "Development", "Design").
        # No separate Category model - categories are derived from existing blog posts.
        categories = Blog.objects.filter(
            is_active=True
        ).values_list('name', flat=True).distinct()
        choices = [('', 'All Categories')]
        choices.extend((cat, cat) for cat in categories if cat)
        return choices
