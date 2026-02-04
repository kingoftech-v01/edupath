"""Data models for EduPath Desktop."""

from .user import User, UserProfile
from .course import Course, Category, Instructor, Review

__all__ = [
    "User",
    "UserProfile",
    "Course",
    "Category",
    "Instructor",
    "Review",
]
