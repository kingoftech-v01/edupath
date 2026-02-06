"""
Courses Forms - Course search and review forms.
"""

from django import forms
from .models import Review, Category


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


class ReviewForm(forms.ModelForm):
    """Form for submitting course reviews."""

    class Meta:
        model = Review
        fields = ['rating', 'desc']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'rating-input'}
            ),
            'desc': forms.Textarea(attrs={
                'class': TEXTAREA_CLASSES,
                'placeholder': 'Write your review...',
                'rows': 4
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'desc': 'Your Review'
        }


class CourseSearchForm(forms.Form):
    """Course search and filter form."""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full py-2 px-3 bg-transparent border-0 focus:ring-0 focus:outline-none rounded-md pe-6 h-10',
            'placeholder': 'Search courses...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={'class': INPUT_CLASSES})
    )
    price_range = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Prices'),
            ('free', 'Free'),
            ('0-25', '$0 - $25'),
            ('25-50', '$25 - $50'),
            ('50+', '$50+'),
        ],
        widget=forms.Select(attrs={'class': INPUT_CLASSES})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate categories dynamically to always show current DB state.
        # Using slug as value for URL-friendly filtering (?category=web-dev).
        categories = Category.objects.filter(is_active=True).values_list('slug', 'name')
        self.fields['category'].choices = [('', 'All Categories')] + list(categories)
