"""
Tests for API client.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from api.client import APIClient, APIResponse


class TestAPIClient:
    """Tests for APIClient."""

    def test_client_initialization(self):
        """Test client initialization."""
        client = APIClient("http://localhost:8000")
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 30

    def test_client_base_url_strips_trailing_slash(self):
        """Test base URL strips trailing slash."""
        client = APIClient("http://localhost:8000/")
        assert client.base_url == "http://localhost:8000"

    def test_get_headers_without_token(self):
        """Test headers without auth token."""
        client = APIClient("http://localhost:8000")
        client.auth_handler.get_token = Mock(return_value=None)
        headers = client._get_headers()
        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/json"

    def test_get_headers_with_token(self):
        """Test headers with auth token."""
        client = APIClient("http://localhost:8000")
        client.auth_handler.get_token = Mock(return_value="test_token")
        headers = client._get_headers()
        assert headers["Authorization"] == "Bearer test_token"


class TestAPIResponse:
    """Tests for APIResponse."""

    def test_response_success(self):
        """Test successful response."""
        response = APIResponse(success=True, data={"key": "value"}, status_code=200)
        assert response.success is True
        assert response.data == {"key": "value"}
        assert response.error is None

    def test_response_error(self):
        """Test error response."""
        response = APIResponse(success=False, error="Not found", status_code=404)
        assert response.success is False
        assert response.error == "Not found"

    def test_response_default_values(self):
        """Test default values."""
        response = APIResponse(success=True)
        assert response.data is None
        assert response.error is None
        assert response.status_code == 0
