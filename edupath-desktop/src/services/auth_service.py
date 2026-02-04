"""
Authentication Service.

Handles user authentication, login, logout, and token refresh.
"""

from typing import Optional, Tuple
from dataclasses import dataclass

from api.client import APIClient
from config import Endpoints
from models.user import User, UserProfile


@dataclass
class AuthResult:
    """Authentication result."""

    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class AuthService:
    """Authentication service."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self._current_user: Optional[User] = None
        self._current_profile: Optional[UserProfile] = None

    async def login(self, username: str, password: str) -> AuthResult:
        """Login user with credentials."""
        response = await self.api_client.post(
            Endpoints.AUTH_LOGIN,
            data={"username": username, "password": password},
        )

        if response.success:
            token_data = response.data
            self.api_client.auth_handler.save_token(
                access_token=token_data.get("access"),
                refresh_token=token_data.get("refresh"),
            )

            # Fetch user data
            user_result = await self.get_current_user()
            if user_result:
                return AuthResult(success=True, user=user_result)

        return AuthResult(
            success=False,
            error=response.error or "Login failed",
        )

    async def logout(self):
        """Logout current user."""
        # Clear local state
        self._current_user = None
        self._current_profile = None
        self.api_client.auth_handler.clear_token()

    async def refresh_token(self) -> bool:
        """Refresh authentication token."""
        refresh_token = self.api_client.auth_handler.get_refresh_token()
        if not refresh_token:
            return False

        response = await self.api_client.post(
            Endpoints.AUTH_REFRESH,
            data={"refresh": refresh_token},
        )

        if response.success:
            self.api_client.auth_handler.save_token(
                access_token=response.data.get("access"),
                refresh_token=refresh_token,
            )
            return True

        return False

    async def get_current_user(self) -> Optional[User]:
        """Get current authenticated user."""
        if self._current_user:
            return self._current_user

        response = await self.api_client.get(Endpoints.CURRENT_USER)
        if response.success and response.data:
            self._current_user = User(**response.data)
            return self._current_user

        return None

    async def get_current_profile(self) -> Optional[UserProfile]:
        """Get current user's profile."""
        if self._current_profile:
            return self._current_profile

        response = await self.api_client.get(Endpoints.USER_PROFILE)
        if response.success and response.data:
            self._current_profile = UserProfile(**response.data)
            return self._current_profile

        return None

    async def update_profile(self, data: dict) -> Tuple[bool, Optional[str]]:
        """Update current user's profile."""
        response = await self.api_client.patch(Endpoints.USER_PROFILE, data=data)
        if response.success:
            self._current_profile = None  # Clear cache
            return True, None
        return False, response.error

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.api_client.auth_handler.is_authenticated()

    @property
    def current_user(self) -> Optional[User]:
        """Get cached current user."""
        return self._current_user
