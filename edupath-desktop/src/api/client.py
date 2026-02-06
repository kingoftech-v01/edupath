"""HTTP client for EduPath API."""

import asyncio
from typing import Any, Optional
from dataclasses import dataclass

import httpx

from .auth import AuthHandler


@dataclass
class APIResponse:
    """Unified response wrapper for all API calls."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    status_code: int = 0


class APIClient:
    """Async HTTP client with JWT auth support."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.auth_handler = AuthHandler()
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Lazily create client (reused across requests for connection pooling)."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        token = self.auth_handler.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def get(self, endpoint: str, params: Optional[dict] = None) -> APIResponse:
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

    async def post(self, endpoint: str, data: Optional[dict] = None) -> APIResponse:
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

    async def patch(self, endpoint: str, data: Optional[dict] = None) -> APIResponse:
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
        try:
            data = response.json() if response.content else None
        except Exception:
            data = None

        if response.is_success:
            return APIResponse(success=True, data=data, status_code=response.status_code)
        else:
            error = data.get("detail", "Request failed") if isinstance(data, dict) else "Request failed"
            return APIResponse(success=False, data=data, error=error, status_code=response.status_code)

    async def close(self):
        """Release network resources. Call on app shutdown."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
