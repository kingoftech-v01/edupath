"""
Validators.

Input validation utilities.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address format."""
    if not email:
        return False, "Email is required"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, ""


def validate_password(password: str, min_length: int = 10) -> Tuple[bool, str]:
    """Validate password strength (must match backend's 10-char minimum)."""
    if not password:
        return False, "Password is required"

    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format."""
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, "Username can only contain letters, numbers, and underscores"

    return True, ""
