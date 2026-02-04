"""
Tests for blog forms.
"""

import pytest

from blog.forms import BlogSearchForm


@pytest.mark.django_db
class TestBlogSearchForm:
    """Tests for BlogSearchForm."""

    def test_form_all_fields_optional(self):
        """Test all fields are optional."""
        form = BlogSearchForm(data={})
        assert form.is_valid()

    def test_form_with_search(self):
        """Test form with search query."""
        form = BlogSearchForm(data={
            'search': 'Python'
        })
        assert form.is_valid()

    def test_form_category_choices(self, blog):
        """Test category choices are populated from database."""
        form = BlogSearchForm()
        choices = form.fields['category'].choices
        assert ('', 'All Categories') in choices

    def test_form_search_max_length(self):
        """Test search field max length."""
        form = BlogSearchForm()
        assert form.fields['search'].max_length == 100
