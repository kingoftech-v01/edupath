"""
Authentication Handler.

Manages JWT tokens and authentication state.
"""

from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

import keyring


SERVICE_NAME = "edupath_desktop"


@dataclass
class TokenData:
    """JWT token data."""

    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None


class AuthHandler:
    """Handles authentication tokens securely."""

    def __init__(self):
        self._token_data: Optional[TokenData] = None
        self._load_saved_token()

    def _load_saved_token(self):
        """Load saved token from secure storage."""
        try:
            saved = keyring.get_password(SERVICE_NAME, "token_data")
            if saved:
                data = json.loads(saved)
                expires_at = None
                if data.get("expires_at"):
                    expires_at = datetime.fromisoformat(data["expires_at"])
                self._token_data = TokenData(
                    access_token=data["access_token"],
                    refresh_token=data.get("refresh_token"),
                    expires_at=expires_at,
                )
        except Exception:
            self._token_data = None

    def save_token(self, access_token: str, refresh_token: Optional[str] = None, expires_in: int = 3600):
        """Save authentication token."""
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        self._token_data = TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )

        # Save to secure storage
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat(),
        }
        keyring.set_password(SERVICE_NAME, "token_data", json.dumps(data))

    def get_token(self) -> Optional[str]:
        """Get current access token if valid."""
        if self._token_data and self._token_data.access_token:
            if self._token_data.expires_at:
                if datetime.now() < self._token_data.expires_at:
                    return self._token_data.access_token
            else:
                return self._token_data.access_token
        return None

    def get_refresh_token(self) -> Optional[str]:
        """Get refresh token."""
        if self._token_data:
            return self._token_data.refresh_token
        return None

    def is_token_expired(self) -> bool:
        """Check if token is expired."""
        if not self._token_data or not self._token_data.expires_at:
            return True
        return datetime.now() >= self._token_data.expires_at

    def clear_token(self):
        """Clear authentication token."""
        self._token_data = None
        try:
            keyring.delete_password(SERVICE_NAME, "token_data")
        except Exception:
            pass

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.get_token() is not None
