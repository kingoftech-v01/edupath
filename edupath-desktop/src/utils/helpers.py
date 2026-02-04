"""
Helper Functions.

General utility functions.
"""

from datetime import datetime
from typing import Optional


def format_date(dt: Optional[datetime], format_str: str = "%B %d, %Y") -> str:
    """Format datetime to string."""
    if not dt:
        return ""
    return dt.strftime(format_str)


def format_duration(hours: int) -> str:
    """Format duration in hours to readable string."""
    if hours < 1:
        return "< 1 hour"
    elif hours == 1:
        return "1 hour"
    else:
        return f"{hours} hours"


def format_number(num: int) -> str:
    """Format number with K/M suffix."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
