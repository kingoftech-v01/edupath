"""
EduPath Forms - Django forms for user interactions.

Provides forms for:
- Authentication (login, signup, password reset)
- Contact submissions
- Reviews
- Course search/filtering
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactSubmission, Review


# =============================================================================
# BASE FORM STYLING
# =============================================================================

# Tailwind CSS classes for form inputs
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


# =============================================================================
# AUTHENTICATION FORMS
# =============================================================================

class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form with styling."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = INPUT_CLASSES
            # Add placeholders
            placeholders = {
                'username': 'Username',
                'email': 'Email',
                'first_name': 'First Name',
                'last_name': 'Last Name',
                'password1': 'Password',
                'password2': 'Confirm Password',
            }
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Enhanced login form with remember me option."""
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'remember_me':
                field.widget.attrs['class'] = INPUT_CLASSES
                # Add placeholders
                if field_name == 'username':
                    field.widget.attrs['placeholder'] = 'Username or Email'
                elif field_name == 'password':
                    field.widget.attrs['placeholder'] = 'Password'


class PasswordResetRequestForm(forms.Form):
    """Password reset request form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter your email address'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            # Don't reveal if email exists - security best practice
            pass
        return email


# =============================================================================
# CONTACT FORMS
# =============================================================================

class ContactForm(forms.ModelForm):
    """Contact form for user inquiries."""

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


# =============================================================================
# REVIEW FORMS
# =============================================================================

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


# =============================================================================
# SEARCH & FILTER FORMS
# =============================================================================

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
        widget=forms.Select(attrs={
            'class': INPUT_CLASSES
        })
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
        widget=forms.Select(attrs={
            'class': INPUT_CLASSES
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate categories from database
        from .models import Category
        categories = Category.objects.filter(is_active=True).values_list('slug', 'name')
        self.fields['category'].choices = [('', 'All Categories')] + list(categories)


class BlogSearchForm(forms.Form):
    """Blog search form."""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Search blogs...'
        })
    )
    category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Category'
        })
    )


# =============================================================================
# NEWSLETTER FORM
# =============================================================================

class NewsletterForm(forms.Form):
    """Newsletter subscription form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter your email'
        })
    )
