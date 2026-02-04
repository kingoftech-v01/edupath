"""API module for EduPath Desktop."""

from .client import APIClient
from .auth import AuthHandler

__all__ = ["APIClient", "AuthHandler"]
