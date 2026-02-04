"""
Tests for courses forms.
"""

import pytest

from courses.forms import ReviewForm, CourseSearchForm


@pytest.mark.django_db
class TestReviewForm:
    """Tests for ReviewForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = ReviewForm(data={
            'rating': 5,
            'desc': 'Great course!'
        })
        assert form.is_valid()

    def test_form_invalid_rating(self):
        """Test form with invalid rating."""
        form = ReviewForm(data={
            'rating': 10,  # Invalid - must be 1-5
            'desc': 'Great course!'
        })
        assert not form.is_valid()

    def test_form_missing_rating(self):
        """Test form with missing rating."""
        form = ReviewForm(data={
            'desc': 'Great course!'
        })
        assert not form.is_valid()
        assert 'rating' in form.errors

    def test_form_fields(self):
        """Test form has correct fields."""
        form = ReviewForm()
        assert 'rating' in form.fields
        assert 'desc' in form.fields

    def test_form_rating_widget(self):
        """Test rating field uses RadioSelect widget."""
        form = ReviewForm()
        from django.forms import RadioSelect
        assert isinstance(form.fields['rating'].widget, RadioSelect)


@pytest.mark.django_db
class TestCourseSearchForm:
    """Tests for CourseSearchForm."""

    def test_form_all_fields_optional(self):
        """Test all fields are optional."""
        form = CourseSearchForm(data={})
        assert form.is_valid()

    def test_form_with_search(self):
        """Test form with search query."""
        form = CourseSearchForm(data={
            'search': 'Python'
        })
        assert form.is_valid()

    def test_form_category_choices(self, category):
        """Test category choices are populated from database."""
        form = CourseSearchForm()
        choices = form.fields['category'].choices
        assert ('', 'All Categories') in choices

    def test_form_price_range_choices(self):
        """Test price range has predefined choices."""
        form = CourseSearchForm()
        choices = form.fields['price_range'].choices
        assert ('', 'All Prices') in choices
        assert ('free', 'Free') in choices
