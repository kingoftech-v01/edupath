"""
HTTP API Client.

Handles all HTTP communication with the EduPath API server.
"""

import asyncio
from typing import Any, Optional
from dataclasses import dataclass

import httpx

from .auth import AuthHandler


@dataclass
class APIResponse:
    """
    API response wrapper.

    Provides consistent response format for all API calls.
    Contains success status, data, error message, and HTTP status.
    """

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    status_code: int = 0


class APIClient:
    """
    HTTP client for EduPath API.

    Provides async methods for GET, POST, PATCH, DELETE requests.
    Handles authentication headers and response parsing.
    """

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the API client.

        Args:
            base_url: The base URL for the API server.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auth_handler = AuthHandler()
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Get or create async HTTP client.

        Creates a new client if none exists or previous was closed.

        Returns:
            httpx.AsyncClient: The HTTP client instance.
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    def _get_headers(self) -> dict:
        """
        Get request headers with auth token.

        Adds Content-Type and Authorization headers.

        Returns:
            dict: Headers dictionary for requests.
        """
        headers = {"Content-Type": "application/json"}
        token = self.auth_handler.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def get(self, endpoint: str, params: Optional[dict] = None) -> APIResponse:
        """
        Make GET request.

        Args:
            endpoint: API endpoint path.
            params: Optional query parameters.

        Returns:
            APIResponse: Wrapped response with success status and data.
        """
        try:
            client = await self._get_client()
            response = await client.get(
                endpoint,
                params=params,
                headers=self._get_headers(),
            )
            return self._handle_response(response)
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    async def post(
        self, endpoint: str, data: Optional[dict] = None
    ) -> APIResponse:
        """
        Make POST request.

        Args:
            endpoint: API endpoint path.
            data: Optional JSON body data.

        Returns:
            APIResponse: Wrapped response with success status and data.
        """
        try:
            client = await self._get_client()
            response = await client.post(
                endpoint,
                json=data,
                headers=self._get_headers(),
            )
            return self._handle_response(response)
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    async def patch(
        self, endpoint: str, data: Optional[dict] = None
    ) -> APIResponse:
        """
        Make PATCH request.

        Args:
            endpoint: API endpoint path.
            data: Optional JSON body data.

        Returns:
            APIResponse: Wrapped response with success status and data.
        """
        try:
            client = await self._get_client()
            response = await client.patch(
                endpoint,
                json=data,
                headers=self._get_headers(),
            )
            return self._handle_response(response)
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    async def delete(self, endpoint: str) -> APIResponse:
        """
        Make DELETE request.

        Args:
            endpoint: API endpoint path.

        Returns:
            APIResponse: Wrapped response with success status.
        """
        try:
            client = await self._get_client()
            response = await client.delete(
                endpoint,
                headers=self._get_headers(),
            )
            return self._handle_response(response)
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def _handle_response(self, response: httpx.Response) -> APIResponse:
        """
        Handle HTTP response.

        Parses JSON response and wraps in APIResponse.

        Args:
            response: The httpx Response object.

        Returns:
            APIResponse: Wrapped response with parsed data.
        """
        try:
            data = response.json() if response.content else None
        except Exception:
            data = None

        if response.is_success:
            return APIResponse(
                success=True,
                data=data,
                status_code=response.status_code,
            )
        else:
            error = data.get("detail", "Request failed") if isinstance(data, dict) else "Request failed"
            return APIResponse(
                success=False,
                data=data,
                error=error,
                status_code=response.status_code,
            )

    async def close(self):
        """
        Close the HTTP client.

        Releases network resources. Should be called on shutdown.
        """
        if self._client and not self._client.is_closed:
            await self._client.aclose()
