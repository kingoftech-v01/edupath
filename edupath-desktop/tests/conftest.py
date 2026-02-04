"""
Pytest configuration and fixtures for EduPath Desktop tests.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from PyQt6.QtWidgets import QApplication

# Create QApplication for tests
@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_api_client():
    """Create mock API client."""
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    client.auth_handler = Mock()
    client.auth_handler.get_token.return_value = "test_token"
    client.auth_handler.is_authenticated.return_value = True
    return client


@pytest.fixture
def mock_auth_service(mock_api_client):
    """Create mock auth service."""
    from services.auth_service import AuthService
    service = AuthService(mock_api_client)
    return service


@pytest.fixture
def mock_cache_service(tmp_path):
    """Create mock cache service."""
    from services.cache_service import CacheService
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    db_path = tmp_path / "test.db"
    return CacheService(cache_dir, db_path)


@pytest.fixture
def mock_course_service(mock_api_client, mock_cache_service):
    """Create mock course service."""
    from services.course_service import CourseService
    return CourseService(mock_api_client, mock_cache_service)


@pytest.fixture
def sample_course():
    """Create sample course data."""
    return {
        "id": 1,
        "title": "Test Course",
        "slug": "test-course",
        "desc": "Test description",
        "price": "49.99",
        "is_free": False,
        "lessons": 10,
        "students": 100,
        "duration_hours": 5,
        "is_active": True,
        "is_featured": True,
    }


@pytest.fixture
def sample_category():
    """Create sample category data."""
    return {
        "id": 1,
        "name": "Development",
        "slug": "development",
        "description": "Development courses",
        "course_count": 10,
        "is_active": True,
    }


@pytest.fixture
def sample_user():
    """Create sample user data."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "is_staff": False,
        "is_superuser": False,
    }
