"""
Application Configuration.

Manages settings, environment variables, and constants.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # API Settings
    API_BASE_URL: str = os.getenv("EDUPATH_API_URL", "http://localhost:8000")
    API_TIMEOUT: int = int(os.getenv("EDUPATH_API_TIMEOUT", "30"))

    # Application Settings
    APP_NAME: str = "EduPath Desktop"
    APP_VERSION: str = "1.0.0"

    # Paths
    APP_DIR: Path = Path.home() / ".edupath"
    CACHE_DIR: Path = APP_DIR / "cache"
    DATA_DIR: Path = APP_DIR / "data"
    LOG_DIR: Path = APP_DIR / "logs"

    # Database
    DB_PATH: Path = DATA_DIR / "edupath.db"

    # Cache Settings
    CACHE_EXPIRY_HOURS: int = 24
    MAX_CACHE_SIZE_MB: int = 100

    # UI Settings
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 800
    MIN_WINDOW_WIDTH: int = 800
    MIN_WINDOW_HEIGHT: int = 600

    def __post_init__(self):
        """Create necessary directories and validate configuration."""
        for directory in [self.APP_DIR, self.CACHE_DIR, self.DATA_DIR, self.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # Warn if API URL is not HTTPS in production
        if (
            not self.API_BASE_URL.startswith("https://")
            and "localhost" not in self.API_BASE_URL
            and "127.0.0.1" not in self.API_BASE_URL
        ):
            import warnings
            warnings.warn(
                f"API_BASE_URL ({self.API_BASE_URL}) is not using HTTPS. "
                "This is insecure for non-local connections. Set EDUPATH_API_URL to an https:// URL.",
                stacklevel=2,
            )


# Global config instance
config = Config()


# API Endpoints
class Endpoints:
    """API endpoint URLs."""

    # Authentication
    AUTH_LOGIN = "/accounts/api/v1/auth/login/"
    AUTH_LOGOUT = "/accounts/api/v1/auth/logout/"
    AUTH_REFRESH = "/accounts/api/v1/auth/token/refresh/"

    # User
    CURRENT_USER = "/accounts/api/v1/me/"
    USER_PROFILE = "/accounts/api/v1/profiles/me/"

    # Courses
    COURSES = "/courses/api/v1/courses/"
    COURSES_FEATURED = "/courses/api/v1/courses/featured/"
    COURSES_FREE = "/courses/api/v1/courses/free/"
    CATEGORIES = "/courses/api/v1/categories/"
    INSTRUCTORS = "/courses/api/v1/instructors/"
    REVIEWS = "/courses/api/v1/reviews/"

    # Blog
    BLOG_POSTS = "/blog/api/v1/posts/"
    BLOG_RECENT = "/blog/api/v1/posts/recent/"

    # Core
    HOMEPAGE_DATA = "/core/api/v1/homepage/"
    SITE_CONFIG = "/core/api/v1/site-config/"
    CONTACT = "/core/api/v1/contact/"
    FEATURES = "/core/api/v1/features/"
    STATISTICS = "/core/api/v1/statistics/"
    PRICING = "/core/api/v1/pricing/"
