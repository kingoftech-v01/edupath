"""
User models.

Pydantic models for user data.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model."""

    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    is_staff: bool = False
    is_superuser: bool = False
    date_joined: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.username


class UserProfile(BaseModel):
    """User profile model."""

    id: int
    user: int
    avatar: Optional[str] = None
    bio: Optional[str] = ""
    phone: Optional[str] = ""
    website: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    twitter_url: Optional[str] = ""
    github_url: Optional[str] = ""
    email_notifications: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
