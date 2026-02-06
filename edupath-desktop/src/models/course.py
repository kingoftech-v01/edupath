"""Course-related Pydantic models."""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class Category(BaseModel):
    """Course category."""
    id: int
    name: str
    slug: str
    icon: Optional[str] = ""
    description: Optional[str] = ""
    course_count: int = 0
    is_active: bool = True


class Instructor(BaseModel):
    """Course instructor with social links."""
    id: int
    name: str
    slug: str
    title: Optional[str] = ""
    bio: Optional[str] = ""
    img: Optional[str] = None
    facebook_url: Optional[str] = ""
    instagram_url: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    twitter_url: Optional[str] = ""
    is_active: bool = True


class Course(BaseModel):
    """Course with pricing, media, and relationships."""
    id: int
    title: str
    slug: str
    name: Optional[str] = ""
    desc: str
    price: Decimal = Decimal("0.00")
    is_free: bool = False
    img: Optional[str] = None
    video_url: Optional[str] = ""
    lessons: int = 0
    students: int = 0
    duration_hours: int = 0
    category: Optional[Category] = None
    instructor: Optional[Instructor] = None
    is_featured: bool = False
    is_active: bool = True
    created_at: Optional[datetime] = None

    @property
    def formatted_price(self) -> str:
        if self.is_free or self.price == 0:
            return "$0"
        return f"${self.price:.0f}"


class Review(BaseModel):
    """Course review with rating."""
    id: int
    name: str
    title: Optional[str] = "Student"
    desc: str
    rating: int
    img: Optional[str] = None
    course: Optional[int] = None
    user: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
