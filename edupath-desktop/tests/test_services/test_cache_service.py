"""
Tests for cache service.
"""

import pytest
from datetime import datetime, timedelta

from services.cache_service import CacheService
from models.course import Course, Category


class TestCacheService:
    """Tests for CacheService."""

    def test_set_and_get(self, mock_cache_service):
        """Test basic set and get."""
        mock_cache_service.set("test_key", {"value": "data"})
        result = mock_cache_service.get("test_key")
        assert result == {"value": "data"}

    def test_get_nonexistent_key(self, mock_cache_service):
        """Test getting nonexistent key returns None."""
        result = mock_cache_service.get("nonexistent")
        assert result is None

    def test_delete(self, mock_cache_service):
        """Test delete."""
        mock_cache_service.set("test_key", "value")
        mock_cache_service.delete("test_key")
        result = mock_cache_service.get("test_key")
        assert result is None

    def test_clear(self, mock_cache_service):
        """Test clear all."""
        mock_cache_service.set("key1", "value1")
        mock_cache_service.set("key2", "value2")
        mock_cache_service.clear()
        assert mock_cache_service.get("key1") is None
        assert mock_cache_service.get("key2") is None

    def test_cache_courses(self, mock_cache_service, sample_course):
        """Test caching courses."""
        courses = [Course(**sample_course)]
        mock_cache_service.cache_courses("test_courses", courses)

        result = mock_cache_service.get_courses("test_courses")
        assert len(result) == 1
        assert result[0].title == "Test Course"

    def test_cache_single_course(self, mock_cache_service, sample_course):
        """Test caching single course."""
        course = Course(**sample_course)
        mock_cache_service.cache_course(course)

        result = mock_cache_service.get_course("test-course")
        assert result is not None
        assert result.slug == "test-course"

    def test_cache_categories(self, mock_cache_service, sample_category):
        """Test caching categories."""
        categories = [Category(**sample_category)]
        mock_cache_service.cache_categories(categories)

        result = mock_cache_service.get_categories()
        assert len(result) == 1
        assert result[0].name == "Development"
